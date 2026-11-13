// ==UserScript==
// @name         Sketchfab STL / OBJ Download (Local Helper)
// @namespace    local.sketchfabdl
// @version      1.0.0
// @description  Download public viewer geometry as STL, OBJ and GLB using your local helper. No Sketchfab login.
// @match        https://sketchfab.com/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @noframes
// @run-at       document-idle
// ==/UserScript==

(() => {
    'use strict';
    const button = document.createElement('button');
    button.textContent = 'Download STL / OBJ';
    Object.assign(button.style, {
        position: 'fixed', bottom: '24px', right: '24px', zIndex: '2147483647',
        padding: '13px 20px', borderRadius: '8px', border: '1px solid #ffffff55',
        background: '#126a89', color: 'white', font: 'bold 14px system-ui',
        boxShadow: '0 3px 16px #0006', cursor: 'pointer'
    });
    document.body.append(button);
    let busy = false;
    const getUid = () => location.pathname.match(/(?:^|[-/])([0-9a-f]{32})(?:\/|$)/)?.[1];
    const update = () => { button.hidden = !getUid(); };
    setInterval(update, 800);
    update();

    button.addEventListener('click', () => {
        const uid = getUid();
        if (!uid || busy) return;
        busy = true;
        button.disabled = true;
        button.textContent = 'Preparing model…';
        const reset = () => {
            busy = false; button.disabled = false;
            button.textContent = 'Download STL / OBJ';
        };
        GM_xmlhttpRequest({
            method: 'POST', url: 'http://127.0.0.1:8765/download',
            headers: { 'Content-Type': 'application/json', 'X-Sketchfabdl': '1' },
            data: JSON.stringify({ uid }), responseType: 'arraybuffer', timeout: 240000,
            onload: response => {
                try {
                    if (response.status !== 200) {
                        const message = new TextDecoder().decode(response.response);
                        let detail = message;
                        try { detail = JSON.parse(message).error; } catch (_) {}
                        throw new Error(detail || `HTTP ${response.status}`);
                    }
                    const match = response.responseHeaders.match(/filename="([^"\r\n]+)"/i);
                    const url = URL.createObjectURL(new Blob([response.response], { type: 'application/zip' }));
                    const link = document.createElement('a');
                    link.href = url; link.download = match?.[1] || `${uid}.zip`;
                    document.body.append(link); link.click(); link.remove();
                    setTimeout(() => URL.revokeObjectURL(url), 60000);
                } catch (error) { alert(`Model download failed: ${error.message}`); }
                finally { reset(); }
            },
            onerror: () => {
                alert('The local converter is unavailable. Run Start Sketchfab Helper.cmd from C:\\Users\\Admin\\sketchfabdl, then try again.');
                reset();
            },
            ontimeout: () => { alert('Download timed out. Check the local helper window.'); reset(); }
        });
    });
})();
