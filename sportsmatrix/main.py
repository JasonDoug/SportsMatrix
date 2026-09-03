"""
SportsMatrix: Unified Sports Prediction & Analytics Platform API
Powered by FastAPI & Pydantic AI. Integrates Moneyball (MLB), NetPredict (Basketball),
NoFreeLocks (NFL), SaturdaySlate (College Football), and Settings & Provider Management.
"""

import os
import sys
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import SportsMatrix Routers
from sportsmatrix.routers import mlb, basketball, nfl, cfb, chat, settings

app = FastAPI(
    title="SportsMatrix Unified REST API & Pydantic AI Service",
    description=(
        "Unified Multi-Sport AI Prediction Platform integrating:\n"
        "- **Moneyball**: MLB Baseball Machine Learning & Monte Carlo Simulator\n"
        "- **NetPredict**: Basketball Analytics (NBA, WNBA, NCAAM, NCAAW)\n"
        "- **NoFreeLocks**: NFL Football Engine with LLM Explanations\n"
        "- **SaturdaySlate**: College Football Ratings & Line Edge Detection\n"
        "- **Pydantic AI Chatbot**: LLM Assistant supporting OpenRouter, Local Ollama, Ollama Cloud, OpenAI, Gemini, Anthropic, and Mock/Test engines."
    ),
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include All Sport Service & Settings Routers
app.include_router(chat.router)
app.include_router(settings.router)
app.include_router(mlb.router)
app.include_router(basketball.router)
app.include_router(nfl.router)
app.include_router(cfb.router)


@app.get("/health", tags=["System Health"])
def sportsmatrix_health():
    """System health check across all integrated sport engines."""
    return {
        "status": "healthy",
        "service": "SportsMatrix Unified API",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "moneyball_mlb": "online",
            "netpredict_basketball": "online",
            "nofreelocks_nfl": "online",
            "saturdayslate_cfb": "online",
            "pydantic_ai_chatbot": "online",
            "settings_manager": "online"
        }
    }


@app.get("/", response_class=HTMLResponse, tags=["Dashboard UI"])
def get_sportsmatrix_dashboard():
    """Serves the main SportsMatrix Interactive Web Portal, Pydantic AI Chatbot, and Settings Page."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SportsMatrix 🏆 Unified Sports AI Platform</title>
    <style>
        :root {
            --bg-color: #0b0e14;
            --card-bg: #151921;
            --border-color: #272d38;
            --text-main: #d0d7de;
            --text-bright: #ffffff;
            --text-sub: #8b949e;
            --accent-blue: #388bfd;
            --accent-green: #238636;
            --accent-purple: #8957e5;
            --accent-gold: #d29922;
            --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-family);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }

        .container {
            max-width: 1400px;
            width: 100%;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 15px;
            margin-bottom: 20px;
        }

        .header h1 {
            margin: 0;
            color: var(--text-bright);
            font-size: 26px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .badge-live {
            background-color: #23863633;
            color: #3fb950;
            border: 1px solid #238636;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }

        .nav-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }

        .nav-btn {
            background-color: #1c212b;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 10px 18px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
        }

        .nav-btn.active {
            background-color: var(--accent-blue);
            color: var(--text-bright);
            border-color: #58a6ff;
        }

        .nav-btn.chatbot-btn {
            background-color: #2d1f47;
            border-color: #8957e5;
            color: #d2a8ff;
        }

        .nav-btn.chatbot-btn.active {
            background-color: #8957e5;
            color: #ffffff;
        }

        .nav-btn.settings-btn {
            background-color: #372a15;
            border-color: #d29922;
            color: #f2cc60;
        }

        .nav-btn.settings-btn.active {
            background-color: #d29922;
            color: #ffffff;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }

        /* Chatbot Interface */
        .chat-box {
            display: flex;
            flex-direction: column;
            height: 520px;
            background-color: #0e1117;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.5;
            white-space: pre-wrap;
        }

        .msg-user {
            align-self: flex-end;
            background-color: #1f6feb;
            color: #ffffff;
        }

        .msg-bot {
            align-self: flex-start;
            background-color: #161b22;
            border: 1px solid var(--border-color);
            color: var(--text-main);
        }

        .chat-input-area {
            display: flex;
            gap: 10px;
            padding: 15px;
            background-color: var(--card-bg);
            border-top: 1px solid var(--border-color);
        }

        .chat-input {
            flex: 1;
            background-color: #0d1117;
            border: 1px solid var(--border-color);
            color: var(--text-bright);
            padding: 12px 15px;
            border-radius: 6px;
            font-size: 14px;
        }

        .btn-send {
            background-color: var(--accent-purple);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
        }

        /* Form Grid */
        .form-grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 15px;
        }

        label {
            font-size: 12px;
            color: var(--text-sub);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        input[type="text"], input[type="password"], select {
            background-color: #0d1117;
            border: 1px solid var(--border-color);
            color: var(--text-bright);
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 14px;
        }

        .btn-primary {
            background-color: var(--accent-green);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
        }

        .btn-secondary {
            background-color: #21262d;
            border: 1px solid var(--border-color);
            color: var(--text-bright);
            padding: 10px 18px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
        }

        .meta-tag {
            display: inline-block;
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 4px;
            background-color: #272d38;
            color: #8b949e;
            margin-right: 4px;
        }

        pre {
            background-color: #0d1117;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 13px;
            border: 1px solid var(--border-color);
        }

        .alert-success {
            padding: 10px 15px;
            background-color: #23863633;
            border: 1px solid #238636;
            color: #3fb950;
            border-radius: 6px;
            margin-top: 10px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 SportsMatrix Unified AI Platform <span class="badge-live">ONLINE</span></h1>
            <div style="color: var(--text-sub); font-size: 14px;">FastAPI Gateway & Pydantic AI LLM Agent</div>
        </div>

        <div class="nav-tabs">
            <button class="nav-btn chatbot-btn active" onclick="switchTab('chat-tab')">🤖 Pydantic AI Chatbot</button>
            <button class="nav-btn settings-btn" onclick="switchTab('settings-tab')">⚙️ LLM Provider Settings</button>
            <button class="nav-btn" onclick="switchTab('mlb-tab')">⚾ MLB (Moneyball)</button>
            <button class="nav-btn" onclick="switchTab('bk-tab')">🏀 Basketball (NetPredict)</button>
            <button class="nav-btn" onclick="switchTab('nfl-tab')">🏈 NFL (NoFreeLocks)</button>
            <button class="nav-btn" onclick="switchTab('cfb-tab')">🏈 CFB (SaturdaySlate)</button>
            <button class="nav-btn" onclick="location.href='/docs'">📄 API Docs (/docs)</button>
        </div>

        <!-- TAB 1: PYDANTIC AI CHATBOT -->
        <div id="chat-tab" class="tab-content active">
            <div class="card" style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin:0; color: #d2a8ff;">🤖 SportsMatrix Pydantic AI LLM Assistant</h3>
                    <div style="color: var(--text-sub); font-size: 13px; margin-top: 4px;">
                        Active Provider: <strong id="chat-active-provider" style="color:#ffffff;">-</strong> | Model: <strong id="chat-active-model" style="color:#58a6ff;">-</strong>
                    </div>
                </div>
                <button class="btn-secondary" onclick="switchTab('settings-tab')">⚙️ Change Provider & Model</button>
            </div>

            <div class="chat-box">
                <div class="chat-messages" id="chat-messages">
                    <div class="message msg-bot">
                        Hello! I am <strong>SportsMatrix AI</strong> powered by Pydantic AI. I can query our Moneyball MLB, NetPredict Basketball, NoFreeLocks NFL, and SaturdaySlate CFB engines.<br><br>
                        <em>Examples you can ask:</em><br>
                        • "Who is projected to win the Chiefs vs 49ers NFL game?"<br>
                        • "Show me Moneyball predictions for the MLB slate"<br>
                        • "What are the latest NCAAM basketball predictions?"<br>
                        • "Extract injury news: Patrick Mahomes is probable, Deebo Samuel questionable."
                    </div>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="chat-input" class="chat-input" placeholder="Ask SportsMatrix AI any prediction question..." onkeypress="if(event.key==='Enter') sendChatMessage()">
                    <button class="btn-send" onclick="sendChatMessage()">Ask Agent</button>
                </div>
            </div>
        </div>

        <!-- TAB 2: SETTINGS PAGE -->
        <div id="settings-tab" class="tab-content">
            <div class="card">
                <h3 style="margin-top:0; color: #f2cc60;">⚙️ LLM Provider & API Key Configuration</h3>
                <p style="color: var(--text-sub); font-size: 14px; margin-bottom: 20px;">
                    Configure your working LLM provider (OpenRouter, Local Ollama, Ollama Cloud, OpenAI, Gemini, Anthropic, or Mock) and select available models dynamically.
                </p>

                <div class="form-grid-2">
                    <!-- LEFT COLUMN: PROVIDER & MODEL SELECTION -->
                    <div style="background-color: #0d1117; padding: 20px; border-radius: 8px; border: 1px solid var(--border-color);">
                        <h4 style="margin-top:0; color: var(--text-bright);">1. Active Provider & Model Selection</h4>
                        
                        <div class="form-group">
                            <label>Working LLM Provider</label>
                            <select id="setting-provider" onchange="onProviderChange()">
                                <option value="openrouter">OpenRouter (Cloud Router)</option>
                                <option value="ollama_local">Local Ollama (Local Daemon)</option>
                                <option value="ollama_cloud">Ollama Cloud (Remote Host)</option>
                                <option value="openai">OpenAI (Direct API)</option>
                                <option value="gemini">Google Gemini (Direct API)</option>
                                <option value="anthropic">Anthropic Claude (Direct API)</option>
                                <option value="mock">Mock / Offline Test Mode</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Selected Working Model</label>
                            <div style="display:flex; gap:8px;">
                                <select id="setting-model" style="flex:1;">
                                    <option value="meta-llama/llama-3.3-70b-instruct">Loading models...</option>
                                </select>
                                <button class="btn-secondary" onclick="fetchModelsForCurrentProvider()" title="Refresh Available Models">🔄 Fetch</button>
                            </div>
                            <div style="font-size: 12px; color: var(--text-sub); margin-top: 4px;" id="models-status-lbl">Available models fetched from selected provider.</div>
                        </div>

                        <div style="margin-top: 25px;">
                            <button class="btn-primary" onclick="saveSettingsForm()">💾 Save Configuration</button>
                            <div id="save-alert" class="alert-success">✓ Settings successfully saved & activated!</div>
                        </div>
                    </div>

                    <!-- RIGHT COLUMN: API KEYS & BASE URLS -->
                    <div style="background-color: #0d1117; padding: 20px; border-radius: 8px; border: 1px solid var(--border-color);">
                        <h4 style="margin-top:0; color: var(--text-bright);">2. Provider API Credentials & Endpoints</h4>

                        <div class="form-group">
                            <label>OpenRouter API Key</label>
                            <input type="password" id="key-openrouter" placeholder="sk-or-v1-...">
                        </div>

                        <div class="form-group">
                            <label>Local Ollama Base URL</label>
                            <input type="text" id="url-ollama-local" value="http://localhost:11434">
                        </div>

                        <div class="form-group">
                            <label>Ollama Cloud Base URL</label>
                            <input type="text" id="url-ollama-cloud" value="https://ollama.com">
                        </div>

                        <div class="form-group">
                            <label>Ollama Cloud API Key</label>
                            <input type="password" id="key-ollama-cloud" placeholder="Optional Ollama Cloud Key">
                        </div>

                        <div class="form-group">
                            <label>OpenAI API Key</label>
                            <input type="password" id="key-openai" placeholder="sk-proj-...">
                        </div>

                        <div class="form-group">
                            <label>Google Gemini API Key</label>
                            <input type="password" id="key-gemini" placeholder="AIzaSy...">
                        </div>

                        <div class="form-group">
                            <label>Anthropic API Key</label>
                            <input type="password" id="key-anthropic" placeholder="sk-ant-...">
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: MONEYBALL MLB -->
        <div id="mlb-tab" class="tab-content">
            <div class="card">
                <h3>⚾ Moneyball MLB Engine</h3>
                <p style="color: var(--text-sub);">Daily Slate Predictions, Win Probabilities, and Monte Carlo Matchup Simulator.</p>
                <button class="btn-secondary" onclick="fetchMLB()">Run MLB Slate Engine (/api/v1/mlb/predict)</button>
                <pre id="mlb-out">Click button above to test endpoint...</pre>
            </div>
        </div>

        <!-- TAB 4: NETPREDICT BASKETBALL -->
        <div id="bk-tab" class="tab-content">
            <div class="card">
                <h3>🏀 NetPredict Basketball Engine</h3>
                <p style="color: var(--text-sub);">Four-Factor Basketball Prediction Engine for NBA, WNBA, NCAAM, and NCAAW.</p>
                <div style="display:flex; gap:10px; margin-bottom:10px;">
                    <button class="btn-secondary" onclick="fetchBK('nba')">NBA Predictions</button>
                    <button class="btn-secondary" onclick="fetchBK('wnba')">WNBA Predictions</button>
                    <button class="btn-secondary" onclick="fetchBK('ncaam')">NCAAM Predictions</button>
                    <button class="btn-secondary" onclick="fetchBK('ncaaw')">NCAAW Predictions</button>
                </div>
                <pre id="bk-out">Click a league button above to test endpoint...</pre>
            </div>
        </div>

        <!-- TAB 5: NOFREELOCKS NFL -->
        <div id="nfl-tab" class="tab-content">
            <div class="card">
                <h3>🏈 NoFreeLocks NFL Engine</h3>
                <p style="color: var(--text-sub);">Tabular ML Ensemble + LLM Narrative Explanation Generator.</p>
                <button class="btn-secondary" onclick="fetchNFL()">Predict KC vs SF Matchup (/api/v1/nfl/predict)</button>
                <pre id="nfl-out">Click button above to test endpoint...</pre>
            </div>
        </div>

        <!-- TAB 6: SATURDAYSLATE CFB -->
        <div id="cfb-tab" class="tab-content">
            <div class="card">
                <h3>🏈 SaturdaySlate College Football Engine</h3>
                <p style="color: var(--text-sub);">Dynamic Elo Ratings, Pre-kickoff Edge Reports, and Monte Carlo Simulations.</p>
                <button class="btn-secondary" onclick="fetchCFBRatings()">Get CFB Ratings (/api/v1/cfb/ratings)</button>
                <button class="btn-secondary" onclick="fetchCFBEdge()">Get Edge Report (/api/v1/cfb/edge-report)</button>
                <pre id="cfb-out">Click button above to test endpoint...</pre>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }

        async function loadSettingsOnPageLoad() {
            try {
                const res = await fetch('/api/v1/settings');
                const cfg = await res.json();

                document.getElementById('setting-provider').value = cfg.active_provider;
                document.getElementById('key-openrouter').value = cfg.openrouter_api_key || '';
                document.getElementById('url-ollama-local').value = cfg.ollama_local_base_url || 'http://localhost:11434';
                document.getElementById('url-ollama-cloud').value = cfg.ollama_cloud_base_url || 'https://ollama.com';
                document.getElementById('key-ollama-cloud').value = cfg.ollama_cloud_api_key || '';
                document.getElementById('key-openai').value = cfg.openai_api_key || '';
                document.getElementById('key-gemini').value = cfg.gemini_api_key || '';
                document.getElementById('key-anthropic').value = cfg.anthropic_api_key || '';

                document.getElementById('chat-active-provider').innerText = cfg.active_provider.toUpperCase();
                document.getElementById('chat-active-model').innerText = cfg.selected_model;

                await fetchModelsForCurrentProvider(cfg.selected_model);
            } catch(e) {
                console.error("Error loading settings:", e);
            }
        }

        async function onProviderChange() {
            await fetchModelsForCurrentProvider();
        }

        async function fetchModelsForCurrentProvider(preferredModel = null) {
            const provider = document.getElementById('setting-provider').value;
            const openrouterKey = document.getElementById('key-openrouter').value;
            const ollamaLocalUrl = document.getElementById('url-ollama-local').value;
            const ollamaCloudUrl = document.getElementById('url-ollama-cloud').value;
            const ollamaCloudKey = document.getElementById('key-ollama-cloud').value;

            const lbl = document.getElementById('models-status-lbl');
            lbl.innerText = `Fetching models for ${provider}...`;

            const url = `/api/v1/settings/models?provider=${provider}&openrouter_api_key=${encodeURIComponent(openrouterKey)}&ollama_local_base_url=${encodeURIComponent(ollamaLocalUrl)}&ollama_cloud_base_url=${encodeURIComponent(ollamaCloudUrl)}&ollama_cloud_api_key=${encodeURIComponent(ollamaCloudKey)}`;

            try {
                const res = await fetch(url);
                const data = await res.json();
                
                const selectEl = document.getElementById('setting-model');
                selectEl.innerHTML = '';
                
                (data.models || []).forEach(m => {
                    const opt = document.createElement('option');
                    opt.value = m;
                    opt.innerText = m;
                    selectEl.appendChild(opt);
                });

                if (preferredModel && data.models.includes(preferredModel)) {
                    selectEl.value = preferredModel;
                }

                lbl.innerText = `Fetched ${data.count || 0} models from ${provider}.`;
            } catch(err) {
                lbl.innerText = `Error fetching models: ${err}`;
            }
        }

        async function saveSettingsForm() {
            const cfg = {
                active_provider: document.getElementById('setting-provider').value,
                selected_model: document.getElementById('setting-model').value,
                openrouter_api_key: document.getElementById('key-openrouter').value,
                ollama_local_base_url: document.getElementById('url-ollama-local').value,
                ollama_cloud_base_url: document.getElementById('url-ollama-cloud').value,
                ollama_cloud_api_key: document.getElementById('key-ollama-cloud').value,
                openai_api_key: document.getElementById('key-openai').value,
                gemini_api_key: document.getElementById('key-gemini').value,
                anthropic_api_key: document.getElementById('key-anthropic').value
            };

            const res = await fetch('/api/v1/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(cfg)
            });

            if (res.ok) {
                document.getElementById('save-alert').style.display = 'block';
                setTimeout(() => { document.getElementById('save-alert').style.display = 'none'; }, 4000);
                document.getElementById('chat-active-provider').innerText = cfg.active_provider.toUpperCase();
                document.getElementById('chat-active-model').innerText = cfg.selected_model;
            }
        }

        async function sendChatMessage() {
            const inputEl = document.getElementById('chat-input');
            const text = inputEl.value.trim();
            if (!text) return;

            const msgBox = document.getElementById('chat-messages');
            msgBox.innerHTML += `<div class="message msg-user">${text}</div>`;
            inputEl.value = '';
            msgBox.scrollTop = msgBox.scrollHeight;

            const botThinking = document.createElement('div');
            botThinking.className = 'message msg-bot';
            botThinking.innerText = 'Analyzing sports prediction engines...';
            msgBox.appendChild(botThinking);
            msgBox.scrollTop = msgBox.scrollHeight;

            try {
                const res = await fetch('/api/v1/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: text })
                });
                const data = await res.json();
                
                let metaHtml = '';
                if (data.service_sources && data.service_sources.length > 0) {
                    metaHtml += '<br><br>' + data.service_sources.map(s => `<span class="meta-tag">⚡ ${s}</span>`).join('');
                }

                botThinking.innerHTML = data.response + metaHtml;
            } catch(err) {
                botThinking.innerText = 'Error processing chat query: ' + err;
            }
            msgBox.scrollTop = msgBox.scrollHeight;
        }

        async function fetchMLB() {
            document.getElementById('mlb-out').innerText = 'Loading...';
            const res = await fetch('/api/v1/mlb/predict?date=2025-08-30');
            const data = await res.json();
            document.getElementById('mlb-out').innerText = JSON.stringify(data, null, 2);
        }

        async function fetchBK(league) {
            document.getElementById('bk-out').innerText = `Loading ${league.toUpperCase()}...`;
            const res = await fetch(`/api/v1/basketball/${league}/predictions`);
            const data = await res.json();
            document.getElementById('bk-out').innerText = JSON.stringify(data, null, 2);
        }

        async function fetchNFL() {
            document.getElementById('nfl-out').innerText = 'Loading KC vs SF NFL prediction...';
            const res = await fetch('/api/v1/nfl/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ home_team: 'KC', away_team: 'SF', vegas_spread: -2.5, vegas_total: 47.5, include_explanation: true })
            });
            const data = await res.json();
            document.getElementById('nfl-out').innerText = JSON.stringify(data, null, 2);
        }

        async function fetchCFBRatings() {
            document.getElementById('cfb-out').innerText = 'Loading CFB ratings...';
            const res = await fetch('/api/v1/cfb/ratings?season=2025');
            const data = await res.json();
            document.getElementById('cfb-out').innerText = JSON.stringify(data, null, 2);
        }

        async function fetchCFBEdge() {
            document.getElementById('cfb-out').innerText = 'Loading CFB Edge Report...';
            const res = await fetch('/api/v1/cfb/edge-report?season=2025&week=13');
            const data = await res.json();
            document.getElementById('cfb-out').innerText = JSON.stringify(data, null, 2);
        }

        window.onload = loadSettingsOnPageLoad;
    </script>
</body>
</html>
"""
