/* voice-memory.js — Voice Memory App Core Logic */

document.addEventListener('DOMContentLoaded', () => {

  // ── Constants ───────────────────────────────────────────────────
  const CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages';
  const CLAUDE_MODEL   = 'claude-sonnet-4-6';
  const LS_MEMORIES    = 'vm_memories';
  const LS_SETTINGS    = 'vm_settings';

  const DEFAULT_SETTINGS = {
    apiKey: '',
    recognitionLang: 'hi-IN',
    voiceRate: 1.0,
    voicePitch: 1.0
  };

  // System prompts
  const INTENT_SYSTEM = `You are an intent classifier for a voice memory assistant. The user may speak in Hindi, English, or Hinglish (mix of both).

Classify the input into exactly one intent:
- STORE_MEMORY: User wants to save/remember something. Hindi triggers: "याद कर", "याद रखो", "याद कर लो", "नोट कर", "याद रहे". English triggers: "remember that", "note this", "don't forget", "save this", "record that".
- QUERY_MEMORY: User is asking about stored memories. Hindi triggers: "क्या याद है", "क्या याद किया", "याद है क्या", "मुझे बताओ", "क्या याद है तुम्हें". English triggers: "what did you remember", "what do you know", "tell me what you stored", "remind me".
- GENERAL: Everything else.

Respond with JSON only, no markdown:
{"intent":"STORE_MEMORY"|"QUERY_MEMORY"|"GENERAL"}`;

  const EXTRACT_SYSTEM = `You are a memory extraction assistant. The user spoke something they want to remember.

Extract the core fact, removing command words like "याद कर लो", "remember that", etc. Keep the actual content.
Also suggest 1-3 short tags.

Respond with JSON only, no markdown:
{"fact":"the clean memory text","tags":["tag1","tag2"]}

Examples:
Input: "याद कर लो कि 10 दिन बाद मेरा जन्मदिन है"
Output: {"fact":"10 दिन बाद जन्मदिन है","tags":["जन्मदिन","personal"]}

Input: "Remember that I have a dentist appointment on Friday at 3pm"
Output: {"fact":"Dentist appointment Friday 3pm","tags":["appointment","health"]}`;

  const ANSWER_SYSTEM = `You are a personal memory assistant who speaks in the same language as the user (Hindi, English, or Hinglish).

Answer naturally and concisely based on the stored memories. If nothing is relevant, say so politely. Keep answers under 80 words. Never make up facts not in the memories.

Today's date: ${new Date().toLocaleDateString('en-IN', {dateStyle:'full'})}`;

  // ── State ────────────────────────────────────────────────────────
  const state = {
    recognition: null,
    synthesis: window.speechSynthesis,
    isListening: false,
    isProcessing: false,
    isSpeaking: false,
    currentUtterance: null,
    interimTranscript: '',
    finalTranscript: '',
    memories: [],
    settings: {},
    sortAscending: false
  };

  // ── DOM Refs ─────────────────────────────────────────────────────
  const el = {
    btnMic:           document.getElementById('btn-mic'),
    micRingOuter:     document.querySelector('.mic-ring-outer'),
    statusBar:        document.getElementById('status-bar'),
    statusText:       document.getElementById('status-text'),
    transcriptArea:   document.getElementById('transcript-area'),
    transcriptText:   document.getElementById('transcript-text'),
    memoryList:       document.getElementById('memory-list'),
    memoryCount:      document.getElementById('memory-count'),
    memoryEmptyState: document.getElementById('memory-empty-state'),
    settingsPanel:    document.getElementById('settings-panel'),
    settingsBackdrop: document.getElementById('settings-backdrop'),
    btnSettings:      document.getElementById('btn-settings'),
    btnSaveSettings:  document.getElementById('btn-save-settings'),
    apiKeyInput:      document.getElementById('api-key-input'),
    btnToggleKey:     document.getElementById('btn-toggle-key'),
    recognitionLang:  document.getElementById('recognition-lang'),
    voiceRate:        document.getElementById('voice-rate'),
    voicePitch:       document.getElementById('voice-pitch'),
    rateVal:          document.getElementById('rate-val'),
    pitchVal:         document.getElementById('pitch-val'),
    btnClearAll:      document.getElementById('btn-clear-all'),
    sortToggle:       document.getElementById('sort-toggle'),
    apiKeyWarning:    document.getElementById('api-key-warning'),
    btnOpenSettingsWarn: document.getElementById('btn-open-settings-warn'),
    langLabel:        document.getElementById('lang-label'),
    settingsFeedback: document.getElementById('settings-feedback'),
    textFallback:     document.getElementById('text-fallback'),
    textInput:        document.getElementById('text-input'),
    btnSendText:      document.getElementById('btn-send-text')
  };

  // ════════════════════════════════════════════════════════════════
  // INITIALIZATION
  // ════════════════════════════════════════════════════════════════

  function init() {
    loadSettings();
    loadMemories();
    setupSpeechRecognition();
    setupEventListeners();
    renderMemoryList();
    showStatus('माइक दबाओ और बोलो', 'idle');
  }

  // ════════════════════════════════════════════════════════════════
  // STORAGE
  // ════════════════════════════════════════════════════════════════

  function loadSettings() {
    try {
      const saved = JSON.parse(localStorage.getItem(LS_SETTINGS) || '{}');
      state.settings = { ...DEFAULT_SETTINGS, ...saved };
    } catch {
      state.settings = { ...DEFAULT_SETTINGS };
    }
    // Populate settings UI
    el.apiKeyInput.value      = state.settings.apiKey ? '••••••••' : '';
    el.recognitionLang.value  = state.settings.recognitionLang;
    el.voiceRate.value        = state.settings.voiceRate;
    el.voicePitch.value       = state.settings.voicePitch;
    el.rateVal.textContent    = state.settings.voiceRate;
    el.pitchVal.textContent   = state.settings.voicePitch;
    el.langLabel.textContent  = state.settings.recognitionLang;

    // Show warning if no API key
    el.apiKeyWarning.hidden = !!state.settings.apiKey;
  }

  function saveSettings() {
    const rawKey  = el.apiKeyInput.value.trim();
    const lang    = el.recognitionLang.value;
    const rate    = parseFloat(el.voiceRate.value);
    const pitch   = parseFloat(el.voicePitch.value);

    // Only update key if user typed something new (not the masked placeholder)
    const newKey = (rawKey && rawKey !== '••••••••') ? rawKey : state.settings.apiKey;

    if (newKey && !newKey.startsWith('sk-ant-')) {
      showSettingsFeedback('API key गलत है। sk-ant- से शुरू होनी चाहिए।', 'err');
      return;
    }

    state.settings = { ...state.settings, apiKey: newKey, recognitionLang: lang, voiceRate: rate, voicePitch: pitch };
    localStorage.setItem(LS_SETTINGS, JSON.stringify(state.settings));

    el.langLabel.textContent   = lang;
    el.apiKeyWarning.hidden    = !!newKey;
    if (state.recognition) state.recognition.lang = lang;

    showSettingsFeedback('Settings save हो गई!', 'ok');
    setTimeout(() => closeSettings(), 1200);
  }

  function loadMemories() {
    try {
      const raw = localStorage.getItem(LS_MEMORIES);
      state.memories = raw ? JSON.parse(raw) : [];
    } catch {
      state.memories = [];
    }
    if (!state.sortAscending) {
      state.memories.sort((a, b) => b.timestamp - a.timestamp);
    }
  }

  function saveMemories() {
    try {
      localStorage.setItem(LS_MEMORIES, JSON.stringify(state.memories));
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        showError('Storage भर गया। कुछ पुरानी यादें हटाओ।');
      }
    }
  }

  // ════════════════════════════════════════════════════════════════
  // SPEECH RECOGNITION
  // ════════════════════════════════════════════════════════════════

  function setupSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      // Fallback for non-Chrome browsers
      el.btnMic.disabled = true;
      el.btnMic.style.opacity = '0.4';
      el.textFallback.hidden = false;
      showStatus('Voice input उपलब्ध नहीं। Chrome use करो या नीचे टाइप करो।', 'error');
      return;
    }

    const rec = new SpeechRecognition();
    rec.continuous      = false;
    rec.interimResults  = true;
    rec.lang            = state.settings.recognitionLang;
    state.recognition   = rec;

    rec.onstart = () => {
      state.isListening = true;
      setMicState('listening');
      showStatus('सुन रहा हूं...', 'listening');
    };

    rec.onresult = (event) => {
      let interim = '';
      let final   = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const t = event.results[i][0].transcript;
        if (event.results[i].isFinal) final += t;
        else interim += t;
      }
      state.interimTranscript = interim;
      if (final) state.finalTranscript += final;
      updateTranscriptDisplay(state.interimTranscript, state.finalTranscript);
    };

    rec.onerror = (event) => {
      const msgs = {
        'not-allowed':    'माइक की permission दो browser settings में।',
        'no-speech':      'कुछ सुनाई नहीं दिया। फिर कोशिश करो।',
        'network':        'Network error। internet check करो।',
        'audio-capture':  'माइक नहीं मिला।',
        'aborted':        null // user stopped manually
      };
      const msg = msgs[event.error];
      if (msg) showError(msg);
      state.isListening = false;
    };

    rec.onend = () => {
      state.isListening = false;
      const transcript = state.finalTranscript.trim();
      if (transcript && !state.isProcessing) {
        processTranscript(transcript);
      } else if (!transcript && !state.isProcessing) {
        showStatus('कुछ सुनाई नहीं दिया। फिर कोशिश करो।', 'muted');
        resetToIdle();
      }
    };
  }

  function startListening() {
    if (state.isProcessing || state.isSpeaking || !state.recognition) return;
    state.finalTranscript   = '';
    state.interimTranscript = '';
    el.transcriptArea.hidden = true;
    el.transcriptText.innerHTML = '';
    state.recognition.lang = state.settings.recognitionLang;
    try {
      state.recognition.start();
    } catch (e) {
      showError('माइक शुरू नहीं हो सका: ' + e.message);
    }
  }

  function stopListening() {
    if (state.recognition && state.isListening) {
      state.recognition.stop();
    }
  }

  // ════════════════════════════════════════════════════════════════
  // CLAUDE API
  // ════════════════════════════════════════════════════════════════

  async function callClaudeAPI(systemPrompt, userMessage, maxTokens = 200, temperature = 0) {
    const key = state.settings.apiKey;
    if (!key) throw new Error('NO_API_KEY');

    const resp = await fetch(CLAUDE_API_URL, {
      method: 'POST',
      headers: {
        'x-api-key':          key,
        'anthropic-version':  '2023-06-01',
        'anthropic-dangerous-direct-browser-calls': 'true',
        'content-type':       'application/json'
      },
      body: JSON.stringify({
        model:      CLAUDE_MODEL,
        max_tokens: maxTokens,
        temperature,
        system:     systemPrompt,
        messages:   [{ role: 'user', content: userMessage }]
      })
    });

    if (!resp.ok) {
      const errData = await resp.json().catch(() => ({}));
      const msg = errData?.error?.message || resp.statusText;
      if (resp.status === 401) throw new Error('API key गलत है। Settings check करो।');
      if (resp.status === 429) throw new Error('बहुत ज्यादा requests। थोड़ा रुको।');
      throw new Error(`API error ${resp.status}: ${msg}`);
    }

    const data = await resp.json();
    return data.content[0].text;
  }

  async function detectIntent(transcript) {
    try {
      const text = await callClaudeAPI(INTENT_SYSTEM, transcript, 60, 0);
      const parsed = JSON.parse(text.trim());
      return parsed.intent || 'GENERAL';
    } catch {
      return 'GENERAL';
    }
  }

  async function extractMemoryFact(transcript) {
    const text = await callClaudeAPI(EXTRACT_SYSTEM, transcript, 150, 0);
    try {
      return JSON.parse(text.trim());
    } catch {
      return { fact: transcript, tags: [] };
    }
  }

  async function answerFromMemories(question, memories) {
    const memoriesStr = memories
      .map((m, i) => `${i+1}. [${m.dateLabel}] ${m.text}`)
      .join('\n');
    const userMsg = `Stored memories:\n${memoriesStr}\n\nUser's question: ${question}`;
    return await callClaudeAPI(ANSWER_SYSTEM, userMsg, 300, 0.3);
  }

  // ════════════════════════════════════════════════════════════════
  // INTENT HANDLERS
  // ════════════════════════════════════════════════════════════════

  async function processTranscript(transcript) {
    if (!state.settings.apiKey) {
      promptForApiKey();
      resetToIdle();
      return;
    }

    state.isProcessing = true;
    setMicState('processing');
    showStatus('सोच रहा हूं...', 'processing');

    try {
      const intent = await detectIntent(transcript);

      if (intent === 'STORE_MEMORY') {
        await handleStoreMemory(transcript);
      } else if (intent === 'QUERY_MEMORY') {
        await handleQueryMemory(transcript);
      } else {
        handleConversation();
      }
    } catch (e) {
      if (e.message === 'NO_API_KEY') {
        promptForApiKey();
      } else {
        showError(e.message);
      }
    } finally {
      state.isProcessing = false;
    }
  }

  async function handleStoreMemory(transcript) {
    const { fact, tags } = await extractMemoryFact(transcript);

    const memory = {
      id:        String(Date.now()),
      text:      fact,
      rawInput:  transcript,
      timestamp: Date.now(),
      dateLabel: new Date().toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' }),
      tags:      Array.isArray(tags) ? tags : []
    };

    state.memories.unshift(memory);
    saveMemories();
    renderMemoryList();

    const confirmMsg = `याद हो गया: ${fact}`;
    updateTranscriptDisplay('', confirmMsg);
    speak(confirmMsg);
    showStatus('याद हो गया!', 'success');
  }

  async function handleQueryMemory(transcript) {
    if (state.memories.length === 0) {
      const msg = 'अभी कोई याद नहीं है। पहले कुछ याद करवाओ।';
      updateTranscriptDisplay('', msg);
      speak(msg);
      resetToIdle();
      return;
    }

    const answer = await answerFromMemories(transcript, state.memories);
    updateTranscriptDisplay('', answer);
    speak(answer);
    showStatus('जवाब दिया', 'success');
  }

  function handleConversation() {
    const msg = 'मैं याद रख सकता हूं। कहो "याद कर लो" और कुछ बताओ, या पूछो "क्या याद है"।';
    updateTranscriptDisplay('', msg);
    speak(msg);
  }

  // ════════════════════════════════════════════════════════════════
  // MEMORY CRUD
  // ════════════════════════════════════════════════════════════════

  function deleteMemory(id) {
    const card = document.querySelector(`[data-memory-id="${id}"]`);
    if (card) {
      card.classList.add('removing');
      setTimeout(() => {
        state.memories = state.memories.filter(m => m.id !== id);
        saveMemories();
        renderMemoryList();
      }, 300);
    }
  }

  function clearAllMemories() {
    if (!confirm('सब यादें हटा दूं? यह वापस नहीं आएंगी।')) return;
    state.memories = [];
    saveMemories();
    renderMemoryList();
  }

  // ════════════════════════════════════════════════════════════════
  // SPEECH SYNTHESIS
  // ════════════════════════════════════════════════════════════════

  function speak(text) {
    if (!text) return;
    state.synthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang  = state.settings.recognitionLang;
    utter.rate  = state.settings.voiceRate;
    utter.pitch = state.settings.voicePitch;

    // Select best matching voice
    const voices = state.synthesis.getVoices();
    const lang   = state.settings.recognitionLang;
    const match  = voices.find(v => v.lang === lang)
                || voices.find(v => v.lang.startsWith(lang.split('-')[0]))
                || null;
    if (match) utter.voice = match;

    utter.onstart = () => {
      state.isSpeaking = true;
      setMicState('speaking');
      showStatus('बोल रहा हूं...', 'speaking');
    };
    utter.onend = () => {
      state.isSpeaking = false;
      resetToIdle();
    };
    utter.onerror = () => {
      state.isSpeaking = false;
      resetToIdle();
    };

    state.currentUtterance = utter;
    state.synthesis.speak(utter);
  }

  function stopSpeaking() {
    state.synthesis.cancel();
    state.isSpeaking = false;
    resetToIdle();
  }

  // ════════════════════════════════════════════════════════════════
  // UI STATE
  // ════════════════════════════════════════════════════════════════

  function setMicState(micState) {
    el.btnMic.className    = `mic-btn ${micState}`;
    el.micRingOuter.className = `mic-ring-outer ${micState === 'listening' ? 'listening' : ''}`;

    const icons = {
      idle:       'fa-microphone',
      listening:  'fa-stop',
      processing: 'fa-circle-notch',
      speaking:   'fa-volume-high'
    };
    const iconEl = el.btnMic.querySelector('i');
    iconEl.className = `fa-solid ${icons[micState] || 'fa-microphone'}`;

    el.btnMic.disabled = (micState === 'processing');
  }

  function resetToIdle() {
    state.isListening  = false;
    state.isProcessing = false;
    state.isSpeaking   = false;
    setMicState('idle');
    showStatus('माइक दबाओ और बोलो', 'idle');
  }

  function showStatus(text, type) {
    el.statusText.textContent = text;
    el.statusBar.className    = `status-bar ${type}`;
  }

  function showError(message) {
    showStatus(message, 'error');
    setMicState('idle');
    state.isProcessing = false;
    state.isSpeaking   = false;
    setTimeout(() => {
      if (el.statusBar.classList.contains('error')) resetToIdle();
    }, 4000);
  }

  function updateTranscriptDisplay(interim, final) {
    el.transcriptArea.hidden = false;
    el.transcriptText.innerHTML =
      (final ? `<span>${escapeHtml(final)}</span>` : '') +
      (interim ? `<span class="interim">${escapeHtml(interim)}</span>` : '');
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // ════════════════════════════════════════════════════════════════
  // MEMORY LIST RENDERING
  // ════════════════════════════════════════════════════════════════

  function renderMemoryList() {
    const count = state.memories.length;
    el.memoryCount.textContent = `यादें (${count})`;

    // Clear existing cards but keep empty state node
    const cards = el.memoryList.querySelectorAll('.memory-card');
    cards.forEach(c => c.remove());

    if (count === 0) {
      el.memoryEmptyState.hidden = false;
      return;
    }

    el.memoryEmptyState.hidden = true;
    const sorted = state.sortAscending
      ? [...state.memories].sort((a, b) => a.timestamp - b.timestamp)
      : [...state.memories].sort((a, b) => b.timestamp - a.timestamp);

    sorted.forEach(mem => {
      el.memoryList.appendChild(createMemoryCard(mem));
    });
  }

  function createMemoryCard(memory) {
    const card = document.createElement('div');
    card.className = 'memory-card';
    card.dataset.memoryId = memory.id;

    const tagsHtml = (memory.tags || [])
      .map(t => `<span class="memory-tag">${escapeHtml(t)}</span>`)
      .join('');

    card.innerHTML = `
      <div class="memory-content">
        <div class="memory-text">${escapeHtml(memory.text)}</div>
        <div class="memory-meta">
          <span>${escapeHtml(memory.dateLabel)}</span>
          ${tagsHtml}
        </div>
      </div>
      <div class="memory-actions">
        <button class="btn-speak-mem" title="सुनो" aria-label="Speak memory">
          <i class="fa-solid fa-volume-high"></i>
        </button>
        <button class="btn-delete-mem" title="हटाओ" aria-label="Delete memory">
          <i class="fa-solid fa-trash"></i>
        </button>
      </div>`;

    card.querySelector('.btn-speak-mem').addEventListener('click', () => speak(memory.text));
    card.querySelector('.btn-delete-mem').addEventListener('click', () => deleteMemory(memory.id));

    return card;
  }

  // ════════════════════════════════════════════════════════════════
  // SETTINGS PANEL
  // ════════════════════════════════════════════════════════════════

  function openSettings() {
    el.settingsPanel.classList.add('open');
    el.settingsBackdrop.classList.add('show');
    el.settingsFeedback.hidden = true;
    // Show actual key hint if set
    if (state.settings.apiKey) {
      const k = state.settings.apiKey;
      el.apiKeyInput.value = k.substring(0, 10) + '...' + k.slice(-4);
    } else {
      el.apiKeyInput.value = '';
    }
  }

  function closeSettings() {
    el.settingsPanel.classList.remove('open');
    el.settingsBackdrop.classList.remove('show');
  }

  function promptForApiKey() {
    el.apiKeyWarning.hidden = false;
    openSettings();
    setTimeout(() => el.apiKeyInput.focus(), 350);
  }

  function showSettingsFeedback(msg, type) {
    el.settingsFeedback.textContent = msg;
    el.settingsFeedback.className   = `settings-feedback ${type}`;
    el.settingsFeedback.hidden      = false;
  }

  // ════════════════════════════════════════════════════════════════
  // EVENT LISTENERS
  // ════════════════════════════════════════════════════════════════

  function setupEventListeners() {
    // Mic button
    el.btnMic.addEventListener('click', () => {
      if (state.isSpeaking)        { stopSpeaking(); return; }
      if (state.isListening)       { stopListening(); return; }
      if (!state.isProcessing)     { startListening(); }
    });

    // Settings
    el.btnSettings.addEventListener('click', openSettings);
    el.settingsBackdrop.addEventListener('click', closeSettings);
    el.btnSaveSettings.addEventListener('click', saveSettings);
    el.btnOpenSettingsWarn.addEventListener('click', promptForApiKey);

    // API key toggle visibility
    el.btnToggleKey.addEventListener('click', () => {
      const isPass = el.apiKeyInput.type === 'password';
      el.apiKeyInput.type = isPass ? 'text' : 'password';
      el.btnToggleKey.querySelector('i').className = `fa-solid fa-eye${isPass ? '-slash' : ''}`;
    });

    // Clear key input on focus if it's masked placeholder
    el.apiKeyInput.addEventListener('focus', () => {
      if (el.apiKeyInput.value.includes('...')) el.apiKeyInput.value = '';
    });

    // Clear all memories
    el.btnClearAll.addEventListener('click', clearAllMemories);

    // Sort toggle
    el.sortToggle.addEventListener('click', () => {
      state.sortAscending = !state.sortAscending;
      el.sortToggle.querySelector('i').className = state.sortAscending
        ? 'fa-solid fa-arrow-up-wide-short'
        : 'fa-solid fa-arrow-down-wide-short';
      renderMemoryList();
    });

    // Rate & pitch live update
    el.voiceRate.addEventListener('input', () => {
      el.rateVal.textContent = parseFloat(el.voiceRate.value).toFixed(1);
    });
    el.voicePitch.addEventListener('input', () => {
      el.pitchVal.textContent = parseFloat(el.voicePitch.value).toFixed(1);
    });

    // Text fallback
    if (el.btnSendText) {
      el.btnSendText.addEventListener('click', () => {
        const txt = el.textInput.value.trim();
        if (txt) { el.textInput.value = ''; processTranscript(txt); }
      });
      el.textInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') el.btnSendText.click();
      });
    }

    // Handle voices loaded asynchronously (Chrome)
    if (window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = () => {
        // Voices are now available; nothing needed, speak() calls getVoices() each time
      };
    }
  }

  // ── Start ────────────────────────────────────────────────────────
  init();

});
