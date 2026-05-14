/**
 * Voice AI - app.js
 * Hindi + English Voice Assistant
 * Records audio → sends to server → Whisper STT → Ollama AI → shows text
 */

const API = "http://localhost:5050";

// ── DOM Elements ──────────────────────────────────────────────────────────────
const micBtn         = document.getElementById("micBtn");
const micIcon        = document.getElementById("micIcon");
const micLabel       = document.getElementById("micLabel");
const micRings       = document.getElementById("micRings");
const sendBtn        = document.getElementById("sendBtn");
const speakBtn       = document.getElementById("speakBtn");
const clearBtn       = document.getElementById("clearBtn");
const chatWindow     = document.getElementById("chatWindow");
const welcomeMsg     = document.getElementById("welcomeMsg");
const transcriptBox  = document.getElementById("transcriptBox");
const transcriptText = document.getElementById("transcriptText");
const copyTranscript = document.getElementById("copyTranscript");
const ollamaStatus   = document.getElementById("ollamaStatus");
const ollamaLabel    = document.getElementById("ollamaLabel");
const timer          = document.getElementById("timer");
const timerDisplay   = document.getElementById("timerDisplay");

// ── State ─────────────────────────────────────────────────────────────────────
let mediaRecorder   = null;
let audioChunks     = [];
let isRecording     = false;
let recordingTimer  = null;
let recordingSeconds = 0;
let currentTranscript = "";
let lastAIResponse  = "";
let conversationHistory = [];  // {role, content}[]

// ── Status Check ──────────────────────────────────────────────────────────────
async function checkStatus() {
  try {
    const res = await fetch(`${API}/status`);
    const data = await res.json();
    if (data.ollama) {
      ollamaStatus.className = "status-dot online";
      ollamaLabel.textContent = "Ollama चालू है ✓";
    } else {
      ollamaStatus.className = "status-dot offline";
      ollamaLabel.textContent = "Ollama बंद है";
    }
  } catch {
    ollamaStatus.className = "status-dot offline";
    ollamaLabel.textContent = "Server से connect नहीं";
  }
}

// Check status every 10 seconds
checkStatus();
setInterval(checkStatus, 10000);

// ── Recording ─────────────────────────────────────────────────────────────────
micBtn.addEventListener("click", () => {
  if (isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
});

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Prefer webm/opus, fallback to default
    const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
      ? "audio/webm;codecs=opus"
      : "audio/webm";

    mediaRecorder = new MediaRecorder(stream, { mimeType });
    audioChunks = [];

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      stream.getTracks().forEach(t => t.stop());
      await processAudio();
    };

    mediaRecorder.start(200); // collect chunks every 200ms
    isRecording = true;

    // Update UI
    micBtn.classList.add("recording");
    micIcon.className = "fa-solid fa-stop";
    micLabel.textContent = "रोकें";
    micRings.classList.add("active");

    // Start timer
    recordingSeconds = 0;
    timer.style.display = "flex";
    updateTimer();
    recordingTimer = setInterval(updateTimer, 1000);

    // Update transcript box
    transcriptText.textContent = "🎙️ सुन रहे हैं... बोलते रहें";
    transcriptBox.classList.add("active");
    copyTranscript.style.display = "none";

  } catch (err) {
    alert("Microphone access nahi mila!\n\nBrowser mein microphone permission dein.\n\nError: " + err.message);
  }
}

function stopRecording() {
  if (mediaRecorder && isRecording) {
    mediaRecorder.stop();
    isRecording = false;

    // Reset UI
    micBtn.classList.remove("recording");
    micIcon.className = "fa-solid fa-microphone";
    micLabel.textContent = "बोलें";
    micRings.classList.remove("active");

    // Stop timer
    clearInterval(recordingTimer);
    timer.style.display = "none";

    transcriptText.textContent = "⏳ Audio process हो रहा है...";
  }
}

function updateTimer() {
  recordingSeconds++;
  const m = Math.floor(recordingSeconds / 60);
  const s = recordingSeconds % 60;
  timerDisplay.textContent = `${m}:${s.toString().padStart(2, "0")}`;
}

// ── Process Audio → Transcribe ────────────────────────────────────────────────
async function processAudio() {
  const blob = new Blob(audioChunks, { type: "audio/webm" });

  if (blob.size < 1000) {
    transcriptText.textContent = "कोई आवाज़ नहीं मिली। फिर कोशिश करें।";
    transcriptBox.classList.remove("active");
    return;
  }

  const formData = new FormData();
  formData.append("audio", blob, "recording.webm");

  try {
    const res = await fetch(`${API}/transcribe`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (data.success && data.transcript.trim()) {
      currentTranscript = data.transcript.trim();
      const langEmoji = getLangEmoji(data.language);

      transcriptText.textContent = `${langEmoji} ${currentTranscript}`;
      transcriptBox.classList.add("active");
      copyTranscript.style.display = "inline-flex";

      sendBtn.disabled = false;
    } else {
      transcriptText.textContent = "समझ नहीं आया। ज़ोर से बोलकर फिर कोशिश करें।";
      transcriptBox.classList.remove("active");
      currentTranscript = "";
    }
  } catch (err) {
    transcriptText.textContent = "Server से connect नहीं हो सका। server चालू है?";
    transcriptBox.classList.remove("active");
    currentTranscript = "";
  }
}

function getLangEmoji(lang) {
  const map = { hi: "🇮🇳", en: "🇺🇸", ur: "🇵🇰", bn: "🇧🇩" };
  return map[lang] || "🌐";
}

// ── Send to AI ────────────────────────────────────────────────────────────────
sendBtn.addEventListener("click", () => {
  if (currentTranscript) sendToAI(currentTranscript);
});

async function sendToAI(text) {
  if (!text.trim()) return;

  // Hide welcome
  if (welcomeMsg) welcomeMsg.style.display = "none";

  // Add user message
  addMessage("user", text);

  // Disable buttons
  sendBtn.disabled = true;
  speakBtn.disabled = true;

  // Show typing indicator
  const typingEl = addTypingIndicator();

  // Add to history
  conversationHistory.push({ role: "user", content: text });

  try {
    const res = await fetch(`${API}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text,
        history: conversationHistory.slice(0, -1), // exclude current
      }),
    });

    const data = await res.json();
    const aiText = data.response || "कोई जवाब नहीं मिला।";

    // Remove typing indicator
    typingEl.remove();

    // Show AI response
    addMessage("ai", aiText);
    lastAIResponse = aiText;
    speakBtn.disabled = false;

    // Add AI to history
    conversationHistory.push({ role: "assistant", content: aiText });

    // Reset transcript
    transcriptText.textContent = "यहाँ आपकी आवाज़ लिखकर आएगी...";
    transcriptBox.classList.remove("active");
    copyTranscript.style.display = "none";
    currentTranscript = "";

  } catch (err) {
    typingEl.remove();
    addMessage("ai", `❌ Error: Server से connect नहीं हो सका।\n\nपक्का करें:\n• voice_server.py चल रही है\n• Ollama install है: https://ollama.com\n• Terminal में चलाएं: ollama run llama3`);
  }
}

// ── Chat Message Rendering ────────────────────────────────────────────────────
function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;

  const now = new Date().toLocaleTimeString("hi-IN", { hour: "2-digit", minute: "2-digit" });
  const icon = role === "user" ? "fa-user" : "fa-robot";
  const name = role === "user" ? "आप" : "Voice AI";

  div.innerHTML = `
    <div class="msg-meta">
      <i class="fa-solid ${icon}"></i>
      <span>${name}</span>
      <span>${now}</span>
    </div>
    <div class="msg-bubble">${escapeHtml(text)}</div>
  `;

  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

function addTypingIndicator() {
  const div = document.createElement("div");
  div.className = "msg ai";
  div.innerHTML = `
    <div class="msg-meta"><i class="fa-solid fa-robot"></i> <span>Voice AI सोच रहा है...</span></div>
    <div class="typing-indicator">
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>
    </div>
  `;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br/>");
}

// ── Speak Response ────────────────────────────────────────────────────────────
speakBtn.addEventListener("click", async () => {
  if (!lastAIResponse) return;

  speakBtn.innerHTML = '<i class="fa-solid fa-volume-high fa-beat"></i> <span>बोल रहे हैं...</span>';
  speakBtn.disabled = true;

  try {
    await fetch(`${API}/speak`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: lastAIResponse }),
    });
  } catch (err) {
    console.error("TTS error:", err);
  } finally {
    setTimeout(() => {
      speakBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i> <span>सुनें</span>';
      speakBtn.disabled = false;
    }, 2000);
  }
});

// ── Copy Transcript ───────────────────────────────────────────────────────────
copyTranscript.addEventListener("click", () => {
  if (currentTranscript) {
    navigator.clipboard.writeText(currentTranscript).then(() => {
      copyTranscript.innerHTML = '<i class="fa-solid fa-check"></i>';
      setTimeout(() => {
        copyTranscript.innerHTML = '<i class="fa-regular fa-copy"></i>';
      }, 1500);
    });
  }
});

// ── Clear Chat ────────────────────────────────────────────────────────────────
clearBtn.addEventListener("click", () => {
  // Remove all messages except welcome
  const msgs = chatWindow.querySelectorAll(".msg");
  msgs.forEach(m => m.remove());

  if (welcomeMsg) welcomeMsg.style.display = "flex";

  conversationHistory = [];
  lastAIResponse = "";
  currentTranscript = "";
  speakBtn.disabled = true;
  sendBtn.disabled = true;
  transcriptText.textContent = "यहाँ आपकी आवाज़ लिखकर आएगी...";
  transcriptBox.classList.remove("active");
  copyTranscript.style.display = "none";
});

// ── Keyboard Shortcut: Space to record ───────────────────────────────────────
document.addEventListener("keydown", (e) => {
  // Space bar = toggle recording (when not in input)
  if (e.code === "Space" && e.target === document.body) {
    e.preventDefault();
    micBtn.click();
  }
  // Enter = send to AI
  if (e.code === "Enter" && !sendBtn.disabled) {
    sendBtn.click();
  }
});
