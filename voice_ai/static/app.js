/**
 * Voice AI — app.js
 * Uses ONLY Windows 11 / Browser built-in APIs:
 *   • SpeechRecognition  → Web Speech API (Chrome/Edge built-in)
 *   • SpeechSynthesis    → Browser TTS (Windows SAPI voices)
 *   • Flask backend      → sirf AI response ke liye
 *
 * LONG SPEECH SUPPORT:
 *   Browser ka Web Speech API ~60s baad khud ruk jaata hai.
 *   Yahan hum NAYA instance banake seamlessly restart karte hain
 *   taaki aap jitna chahein bolte rahein — transcript accumulate hota rahega.
 *
 * Koi install nahi — sirf Python + Edge/Chrome browser chahiye
 */

'use strict';

// ── Config ────────────────────────────────────────────────────────────────────
const SERVER = 'http://localhost:5050';
let currentLang = 'hi-IN';

// ── DOM refs ──────────────────────────────────────────────────────────────────
const micBtn       = document.getElementById('micBtn');
const micIcon      = document.getElementById('micIcon');
const micLabel     = document.getElementById('micLabel');
const micRing      = document.getElementById('micRing');
const sendBtn      = document.getElementById('sendBtn');
const speakBtn     = document.getElementById('speakBtn');
const stopSpeakBtn = document.getElementById('stopSpeakBtn');
const chatWindow   = document.getElementById('chatWindow');
const welcomeCard  = document.getElementById('welcomeCard');
const liveText     = document.getElementById('liveText');
const transcriptBar= document.getElementById('transcriptBar');
const copyBtn      = document.getElementById('copyBtn');
const statusDot    = document.getElementById('statusDot');
const statusLabel  = document.getElementById('statusLabel');
const btnHi        = document.getElementById('btnHi');
const btnEn        = document.getElementById('btnEn');

// ── State ─────────────────────────────────────────────────────────────────────
let recognition       = null;
let isListening       = false;          // USER ka intention — kya sunna chahiye?
let isRestarting      = false;          // auto-restart chal raha hai?

// Transcript accumulator — RESTART ke baad bhi sab preserve rahega
let accumulatedText   = '';             // confirmed final text (sab sessions)
let sessionFinal      = '';             // current session ka confirmed text
let sessionInterim    = '';             // current session ka live/interim text

let lastAIResponse    = '';
let isSpeaking        = false;
let history           = [];

// Timer display
let timerInterval     = null;
let recordingSeconds  = 0;

// ── Speech Recognition API ───────────────────────────────────────────────────
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  setStatus('⚠️ Edge/Chrome mein kholein', 'warn');
  micBtn.disabled = true;
  micLabel.textContent = 'Unsupported';
  alert(
    '❌ Yeh browser Speech Recognition support nahi karta.\n\n' +
    'Microsoft Edge ya Google Chrome mein kholein:\n' +
    'http://localhost:5050'
  );
}

// ── Build a fresh SpeechRecognition instance ─────────────────────────────────
function buildRecognition() {
  const r = new SpeechRecognition();
  r.lang            = currentLang;
  r.interimResults  = true;    // live text chahiye
  r.maxAlternatives = 1;
  r.continuous      = true;    // browser ke andar bhi continuous rakhein

  // First start — sirf agar nayi session hai (restart pe skip)
  r.onstart = () => {
    if (!isRestarting) {
      // Bilkul nayi recording — sab reset
      accumulatedText = '';
      sessionFinal    = '';
      sessionInterim  = '';
      transcriptBar.classList.add('active');
      copyBtn.style.display = 'none';
      sendBtn.disabled = true;
      startTimer();
    }
    isRestarting = false;
    setMicState(true);
    setStatus('🎙️ सुन रहे हैं... बोलते रहें', 'listening');
    renderLive();
  };

  r.onresult = (e) => {
    sessionInterim = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const t = e.results[i][0].transcript;
      if (e.results[i].isFinal) {
        sessionFinal += t;       // space automatically aata hai sentences mein
      } else {
        sessionInterim += t;
      }
    }
    renderLive();
  };

  r.onerror = (e) => {
    console.warn('SpeechRecognition error:', e.error);

    if (e.error === 'not-allowed') {
      isListening = false;
      stopTimer();
      setMicState(false);
      setStatus('❌ Microphone blocked', 'error');
      alert(
        '❌ Microphone access nahi mila!\n\n' +
        'Browser address bar mein 🔒 lock icon click karke\n' +
        'Microphone = Allow karein, phir page refresh karein.'
      );
      return;
    }

    if (e.error === 'aborted') {
      // Manual stop — ignore karo, onend handle karega
      return;
    }

    // no-speech / network / other — agar user abhi bhi sunna chahta hai toh restart
    if (isListening) {
      scheduleRestart();
    }
  };

  r.onend = () => {
    // Session ka final text accumulate karo
    accumulatedText += sessionFinal;
    sessionFinal = '';
    sessionInterim = '';

    if (isListening) {
      // Browser ne khud band kiya (timeout) — restart karo seamlessly
      scheduleRestart();
    } else {
      // User ne khud roka — finish
      onRecordingFinished();
    }
  };

  return r;
}

// ── Seamless restart (browser timeout workaround) ────────────────────────────
function scheduleRestart() {
  if (!isListening) return;
  isRestarting = true;
  setStatus('🔄 जारी रख रहे हैं...', 'listening');

  // Thodi delay — browser ko release karne ka time
  setTimeout(() => {
    if (!isListening) return;
    recognition = buildRecognition();
    try {
      recognition.start();
    } catch (err) {
      console.error('Restart failed:', err);
      // Ek aur try 500ms baad
      setTimeout(() => {
        if (!isListening) return;
        recognition = buildRecognition();
        try { recognition.start(); } catch (_) {
          isListening = false;
          isRestarting = false;
          stopTimer();
          setMicState(false);
          setStatus('⚠️ Dobara mic dabayein', 'warn');
          onRecordingFinished();
        }
      }, 500);
    }
  }, 150);
}

// ── Start / Stop Recording ────────────────────────────────────────────────────
function toggleRecording() {
  if (isListening) {
    stopListening();
  } else {
    startListening();
  }
}

function startListening() {
  if (!SpeechRecognition) return;
  isListening   = true;
  isRestarting  = false;
  accumulatedText = '';
  sessionFinal    = '';
  sessionInterim  = '';

  recognition = buildRecognition();
  try {
    recognition.start();
  } catch (err) {
    console.error(err);
    isListening = false;
    setStatus('❌ Mic shuru nahi hua — dobara koshish karein', 'error');
  }
}

function stopListening() {
  isListening  = false;
  isRestarting = false;
  stopTimer();
  if (recognition) {
    try { recognition.stop(); } catch (_) {}
  }
  setMicState(false);
  // onend pe onRecordingFinished() call hoga
}

function onRecordingFinished() {
  // Saara accumulated + current session ka text
  const fullText = (accumulatedText + sessionFinal + sessionInterim).trim();

  if (!fullText) {
    liveText.textContent = 'कोई आवाज़ नहीं मिली — फिर कोशिश करें';
    transcriptBar.classList.remove('active');
    setStatus('तैयार है', 'idle');
    return;
  }

  // Final state save
  accumulatedText = fullText;
  sessionFinal    = '';
  sessionInterim  = '';

  renderLive();
  copyBtn.style.display = 'inline-flex';
  sendBtn.disabled = false;
  setStatus('✅ बात सुन ली — "AI से पूछें" दबाएँ', 'idle');
}

// ── Live render ───────────────────────────────────────────────────────────────
function renderLive() {
  const confirmed = accumulatedText + sessionFinal;
  const live      = sessionInterim;

  if (!confirmed && !live) {
    liveText.innerHTML = '<span style="opacity:0.4">बोलते रहें...</span>';
    return;
  }

  liveText.innerHTML =
    escHtml(confirmed) +
    (live
      ? '<span style="opacity:0.5; font-style:italic"> ' + escHtml(live) + '</span>'
      : '');
}

// ── Timer ─────────────────────────────────────────────────────────────────────
function startTimer() {
  recordingSeconds = 0;
  const timerEl = document.getElementById('timer');
  const timerDisplay = document.getElementById('timerDisplay');
  if (timerEl) timerEl.style.display = 'flex';
  clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    recordingSeconds++;
    const m = Math.floor(recordingSeconds / 60);
    const s = recordingSeconds % 60;
    if (timerDisplay) timerDisplay.textContent = `${m}:${s.toString().padStart(2,'0')}`;
  }, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
  const timerEl = document.getElementById('timer');
  if (timerEl) timerEl.style.display = 'none';
}

// ── Language Switch ───────────────────────────────────────────────────────────
function setLang(lang) {
  currentLang = lang;
  btnHi.classList.toggle('active', lang === 'hi-IN');
  btnEn.classList.toggle('active', lang === 'en-US');
  preferredVoice = pickVoice(lang);
}

// ── Send to AI ────────────────────────────────────────────────────────────────
async function sendToAI() {
  const text = accumulatedText.trim();
  if (!text) return;

  // Hide welcome card
  if (welcomeCard) welcomeCard.style.display = 'none';

  addMessage('user', text);
  sendBtn.disabled = true;

  // Add to history
  history.push({ role: 'user', content: text });

  // Show thinking indicator
  const thinkEl = addThinking();
  setStatus('🤔 Soch raha hoon...', 'thinking');

  try {
    const res = await fetch(`${SERVER}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, history: history.slice(0, -1) }),
    });
    const data = await res.json();
    const reply = data.response || 'Koi jawab nahi mila.';

    thinkEl.remove();
    addMessage('ai', reply);
    lastAIResponse = reply;
    speakBtn.disabled = false;
    history.push({ role: 'assistant', content: reply });

    // Reset transcript area
    resetTranscriptBar();
    setStatus('✅ Jawab aa gaya', 'idle');

  } catch (err) {
    thinkEl.remove();
    const errMsg =
      '❌ Server se connect nahi hua.\n\n' +
      'start.bat dobara chalayein aur phir koshish karein.';
    addMessage('ai', errMsg);
    setStatus('❌ Server nahi mila', 'error');
  }
}

// ── TTS — Windows Built-in SpeechSynthesis ───────────────────────────────────
let preferredVoice = null;

// Voices load hone ka wait karein
window.speechSynthesis.onvoiceschanged = () => {
  preferredVoice = pickVoice(currentLang);
};

function pickVoice(lang) {
  const voices = window.speechSynthesis.getVoices();
  // Try to match language exactly, then loose match
  return (
    voices.find(v => v.lang === lang) ||
    voices.find(v => v.lang.startsWith(lang.split('-')[0])) ||
    voices[0] ||
    null
  );
}

function speakLastResponse() {
  if (!lastAIResponse) return;
  speakText(lastAIResponse);
}

function speakText(text) {
  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  // Split long text into sentences to avoid browser TTS truncation bug
  const chunks = splitIntoChunks(text, 200);
  let idx = 0;

  isSpeaking = true;
  speakBtn.style.display   = 'none';
  stopSpeakBtn.style.display = 'inline-flex';
  setStatus('🔊 Bol raha hoon...', 'speaking');

  function speakNext() {
    if (idx >= chunks.length || !isSpeaking) {
      onSpeakEnd();
      return;
    }
    const utt = new SpeechSynthesisUtterance(chunks[idx]);
    utt.lang  = currentLang;
    utt.rate  = 0.92;
    utt.pitch = 1.0;
    utt.volume = 1.0;
    if (preferredVoice) utt.voice = preferredVoice;

    utt.onend   = () => { idx++; speakNext(); };
    utt.onerror = (e) => { console.error('TTS error', e); onSpeakEnd(); };

    window.speechSynthesis.speak(utt);
  }

  speakNext();
}

function stopSpeaking() {
  isSpeaking = false;
  window.speechSynthesis.cancel();
  onSpeakEnd();
}

function onSpeakEnd() {
  isSpeaking = false;
  speakBtn.style.display    = 'inline-flex';
  stopSpeakBtn.style.display = 'none';
  setStatus('तैयार है', 'idle');
}

// Long text ko chunks mein todna (browser TTS 200-char limit workaround)
function splitIntoChunks(text, maxLen) {
  const sentences = text.match(/[^।|.!?\n]+[।.!?\n]*/g) || [text];
  const chunks = [];
  let current = '';
  for (const s of sentences) {
    if ((current + s).length > maxLen) {
      if (current) chunks.push(current.trim());
      current = s;
    } else {
      current += s;
    }
  }
  if (current.trim()) chunks.push(current.trim());
  return chunks.length ? chunks : [text];
}

// ── Chat Message Rendering ────────────────────────────────────────────────────
function addMessage(role, text) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;

  const time = new Date().toLocaleTimeString('hi-IN', {
    hour: '2-digit', minute: '2-digit'
  });

  const avatar = role === 'user' ? '🧑' : '🤖';
  const name   = role === 'user' ? 'आप' : 'Voice AI';

  div.innerHTML = `
    <div class="msg-header">
      <span class="msg-avatar">${avatar}</span>
      <span class="msg-name">${name}</span>
      <span class="msg-time">${time}</span>
      ${role === 'ai'
        ? `<button class="msg-speak-btn" onclick="speakText(${JSON.stringify(text)})" title="यह सुनें">🔊</button>`
        : ''}
    </div>
    <div class="msg-bubble">${formatText(escHtml(text))}</div>
  `;

  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

function addThinking() {
  const div = document.createElement('div');
  div.className = 'msg ai thinking';
  div.innerHTML = `
    <div class="msg-header">
      <span class="msg-avatar">🤖</span>
      <span class="msg-name">Voice AI</span>
    </div>
    <div class="msg-bubble">
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="dot"></span>
    </div>
  `;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

// newlines → <br>, **bold** → <strong>
function formatText(html) {
  return html
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br/>');
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function setMicState(on) {
  if (on) {
    micBtn.classList.add('recording');
    micIcon.textContent  = '⏹️';
    micLabel.textContent = 'रोकें';
    micRing.classList.add('active');
  } else {
    micBtn.classList.remove('recording');
    micIcon.textContent  = '🎤';
    micLabel.textContent = 'बोलें';
    micRing.classList.remove('active');
  }
}

function setStatus(msg, state) {
  statusLabel.textContent = msg;
  statusDot.className = 'status-dot ' + (state || 'idle');
}

function resetTranscriptBar() {
  accumulatedText = '';
  sessionFinal    = '';
  sessionInterim  = '';
  liveText.textContent = 'यहाँ आपकी आवाज़ live दिखेगी...';
  transcriptBar.classList.remove('active');
  copyBtn.style.display = 'none';
}

function clearChat() {
  chatWindow.querySelectorAll('.msg').forEach(m => m.remove());
  if (welcomeCard) welcomeCard.style.display = 'flex';
  history       = [];
  lastAIResponse = '';
  speakBtn.disabled = true;
  sendBtn.disabled  = true;
  resetTranscriptBar();
  window.speechSynthesis.cancel();
  setStatus('तैयार है', 'idle');
}

function copyTranscript() {
  const text = accumulatedText.trim();
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    copyBtn.textContent = '✅';
    setTimeout(() => { copyBtn.textContent = '📋'; }, 1500);
  });
}

// ── Keyboard Shortcuts ────────────────────────────────────────────────────────
document.addEventListener('keydown', (e) => {
  // Don't fire if user is typing somewhere
  if (e.target !== document.body) return;

  if (e.code === 'Space') {
    e.preventDefault();
    toggleRecording();
  }
  if (e.code === 'Enter' && !sendBtn.disabled) {
    sendToAI();
  }
  if (e.code === 'KeyS' && !speakBtn.disabled) {
    speakLastResponse();
  }
});

// ── Init ──────────────────────────────────────────────────────────────────────
setStatus('तैयार है', 'idle');
preferredVoice = pickVoice(currentLang);

// Ping server (optional — just to show connected status)
fetch(`${SERVER}/status`)
  .then(r => r.json())
  .then(d => {
    if (d.server === 'running') setStatus('✅ Server चालू है', 'idle');
  })
  .catch(() => {
    // Server nahi bhi chala ho toh TTS browser se hi kaam karega
    setStatus('⚠️ Server नहीं मिला (TTS फिर भी काम करेगा)', 'warn');
  });
