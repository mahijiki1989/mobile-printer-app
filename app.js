document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const fileUpload = document.getElementById('file-upload');
    const previewFrame = document.getElementById('preview-frame');
    const noFileMsg = document.getElementById('no-file-msg');
    
    // Settings Elements
    const scaleInput = document.getElementById('print-scale');
    const scaleVal = document.getElementById('scale-val');
    const marginTop = document.getElementById('margin-top');
    const marginRight = document.getElementById('margin-right');
    const marginBottom = document.getElementById('margin-bottom');
    const marginLeft = document.getElementById('margin-left');
    const bgGraphics = document.getElementById('background-graphics');
    const printBtn = document.getElementById('btn-print');

    // Drawer Elements
    const fabSettings = document.getElementById('fab-settings');
    const settingsDrawer = document.getElementById('settings-drawer');
    const backdrop = document.getElementById('settings-backdrop');

    let currentHtmlContent = '';

    // Mobile UI Toggles
    fabSettings.addEventListener('click', () => {
        settingsDrawer.classList.add('open');
        backdrop.classList.add('show');
    });

    backdrop.addEventListener('click', () => {
        settingsDrawer.classList.remove('open');
        backdrop.classList.remove('show');
    });

    // Handle File Selection (User uploads an HTML file device)
    fileUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            currentHtmlContent = event.target.result;
            noFileMsg.style.display = 'none';
            previewFrame.style.display = 'block';
            renderPreview();
        };
        reader.readAsText(file);
    });

    // Instant Preview Updates when sliders/inputs change
    scaleInput.addEventListener('input', (e) => {
        scaleVal.innerText = `${e.target.value}%`;
        applyPreviewStyles();
    });

    [marginTop, marginRight, marginBottom, marginLeft, bgGraphics].forEach(el => {
        el.addEventListener('input', applyPreviewStyles);
        el.addEventListener('change', applyPreviewStyles);
    });

    // Render the loaded HTML into the iframe
    function renderPreview() {
        const doc = previewFrame.contentDocument || previewFrame.contentWindow.document;
        doc.open();
        doc.write(currentHtmlContent);
        doc.close();
        
        // Ensure styles apply correctly after content loads
        previewFrame.onload = () => {
            applyPreviewStyles();
        };
        // Apply immediately as well
        applyPreviewStyles();
    }

    // This is the core logic: Injects @page margins and scale directly into the HTML preview
    // so when Window.print is called, it inherits these "Desktop" settings.
    function applyPreviewStyles() {
        if (!currentHtmlContent) return;
        
        try {
            const doc = previewFrame.contentDocument || previewFrame.contentWindow.document;
            let styleTag = doc.getElementById('adv-print-styles');
            
            if (!styleTag) {
                styleTag = doc.createElement('style');
                styleTag.id = 'adv-print-styles';
                doc.head.appendChild(styleTag);
            }

            const scale = scaleInput.value / 100;
            const mt = (marginTop.value || 0) + 'cm';
            const mr = (marginRight.value || 0) + 'cm';
            const mb = (marginBottom.value || 0) + 'cm';
            const ml = (marginLeft.value || 0) + 'cm';
            const bg = bgGraphics.checked ? 'exact' : 'auto'; 

            // CSS injected directly into iframe
            styleTag.innerHTML = `
                @page {
                    size: auto;
                    margin: ${mt} ${mr} ${mb} ${ml} !important;
                }
                
                @media print {
                    body {
                        zoom: ${scale} !important;
                        -webkit-print-color-adjust: ${bg} !important;
                        print-color-adjust: ${bg} !important;
                    }
                }

                @media screen {
                    /* Show scaled version for previewing inside the app */
                    body {
                        transform: scale(${scale});
                        transform-origin: top left;
                        padding: ${mt} ${mr} ${mb} ${ml};
                        box-sizing: border-box;
                        width: calc(${100 / scale}% - ${parseFloat(mr) + parseFloat(ml)}cm);
                        overflow-x: hidden;
                    }
                }
            `;
        } catch (err) {
            console.error("Error applying preview styles: ", err);
        }
    }

    // Trigger PDF Flow
    printBtn.addEventListener('click', () => {
        if (!currentHtmlContent) {
            alert('Please select an HTML file first!');
            return;
        }
        
        // Hide Drawer on mobile before print to avoid visual glitches
        settingsDrawer.classList.remove('open');
        backdrop.classList.remove('show');

        // Allow UI to update before blocking execution
        setTimeout(() => {
            const doc = previewFrame.contentDocument || previewFrame.contentWindow.document;
            const element = doc.body;

            // Margins parsing
            const mt = parseFloat(marginTop.value) || 0;
            const mr = parseFloat(marginRight.value) || 0;
            const mb = parseFloat(marginBottom.value) || 0;
            const ml = parseFloat(marginLeft.value) || 0;
            
            // Note: Background graphics is somewhat abstract for html2canvas, 
            // usually background color will render automatically unless specified otherwise.

            // Change button state
            printBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating PDF...';
            printBtn.disabled = true;

            const scaleVal = (parseFloat(scaleInput.value) / 100) * 2; // base resolution 2

            const opt = {
                margin:       [mt, mr, mb, ml], // [top, left, bottom, right] for jsPDF but WAIT: html2pdf order is [top, left, bottom, right] -> actually, css is [top, right, bottom, left], html2pdf uses [top, left, bottom, right] (like jsPDF margin object config).
                filename:     'AdvPrint_Document.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: scaleVal, useCORS: true }, 
                jsPDF:        { unit: 'cm', format: 'a4', orientation: 'portrait' }
            };

            // Fix the html2pdf margin format which acts exactly like jsPDF margins or html2pdf's custom parser: [top, left, bottom, right]
            opt.margin = [mt, ml, mb, mr];

            html2pdf().set(opt).from(element).save().then(() => {
                printBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Save as PDF';
                printBtn.disabled = false;
            }).catch(err => {
                console.error("PDF generation error: ", err);
                alert("Failed to create PDF. " + err);
                printBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Save as PDF';
                printBtn.disabled = false;
            });
        }, 300);
    });
});
