<div class="progression-step"><div><span class="roman-numeral">V<sup>6</sup> &rarr; i</span></div><div class="note-example">Example in A Minor: G#-B-E &rarr; A-C-E</div><div class="note-example">As scale degrees (A=1): (7-2-5) &rarr; (1-&flat;3-5)</div><div class="transformation-desc">Transformation: 5th (E) common; Leading tone (G#&rarr;A) & other voice (B&rarr;C) resolve.</div></div>
                    </div>`
            }
        ];

        function setProgressionTabContent(tabName) {
            const selectedProgression = progressionData.find(p => p.name === tabName);
            if (selectedProgression) {
                progressionTabContentAreaDiv.innerHTML = `<div class="tab-content-panel">${selectedProgression.content}</div>`;
                // Update the transformation examples for the new tab with current tonic
                updateTransformationExamples(currentTonic, currentModeName, tabName);
            } else {
                progressionTabContentAreaDiv.innerHTML = `<div class="tab-content-panel"><p>Content not found.</p></div>`;
            }
        }

        // --- NEW: Function to update transformation examples based on selected tonic note ---
        function updateTransformationExamples(tonic, mode, progressionTabName) {
            if (!progressionTabName) return;

            const selectedTab = progressionData.find(p => p.name === progressionTabName);
            if (!selectedTab) return;

            // Get all progression steps (examples)
            const progressionSteps = document.querySelectorAll('.progression-step');
            
            // Update the examples with the correct notes for the current tonic and mode
            progressionSteps.forEach(step => {
                const noteExampleDivs = step.querySelectorAll('.note-example');
                const transformationDescDiv = step.querySelector('.transformation-desc');
                
                // Update note examples with current tonic
                if (noteExampleDivs.length > 0) {
                    // Different approach depending on selected progression
                    if (progressionTabName === "Generic I Moves") {
                        updateGenericIMoveExamples(step, tonic, mode);
                    } else if (progressionTabName === "I-IV-V-I (Major)") {
                        updateMajorProgressionExamples(step, tonic);
                    } else if (progressionTabName === "i-iv-V-i (Minor)") {
                        updateMinorProgressionExamples(step, tonic);
                    }
                }
            });
        }
        
        // Helper functions for specific progression types
        function updateGenericIMoveExamples(stepElement, tonic, mode) {
            const romanDiv = stepElement.querySelector('.roman-numeral');
            if (!romanDiv) return;
            
            // Get the roman numeral text to determine which progression step we're on
            const romanText = romanDiv.textContent.trim();
            const noteExamples = stepElement.querySelectorAll('.note-example');
            const transformDesc = stepElement.querySelector('.transformation-desc');
            
            // Get scale notes for the current tonic and mode
            const scaleNotes = getScaleNotes(tonic, mode);
            if (scaleNotes.length !== 7) return;
            
            // Get the tonic triad
            const tonicTriad = getModeSpecificTonicTriad(tonic, mode);
            if (!tonicTriad || !tonicTriad.notes) return;
            
            // Each roman numeral text defines a different transformation
            if (romanText.includes("I → V6")) {
                // I → V6 (e.g., C-E-G → B-D-G in C Major)
                const rootIdx = getNoteIndex(tonic);
                const bNote = getNoteFromIndex((rootIdx - 1 + 12) % 12); // 7th degree
                const dNote = getNoteFromIndex((rootIdx + 2) % 12); // 2nd degree
                
                noteExamples[0].innerHTML = `e.g., In ${tonic} ${mode}: ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]} &rarr; ${bNote}-${dNote}-${tonicTriad.notes[2]}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (7-2-5)`;
            } 
            else if (romanText.includes("I → IV6/4")) {
                // I → IV6/4 (e.g., C-E-G → C-F-A in C Major)
                const rootIdx = getNoteIndex(tonic);
                const fNote = getNoteFromIndex((rootIdx + 5) % 12); // 4th degree
                const aNote = getNoteFromIndex((rootIdx + 9) % 12); // 6th degree
                
                noteExamples[0].innerHTML = `e.g., In ${tonic} ${mode}: ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]} &rarr; ${tonicTriad.notes[0]}-${fNote}-${aNote}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (1-4-6)`;
            }
            else if (romanText.includes("I → vi6")) {
                // I → vi6 (e.g., C-E-G → C-E-A in C Major)
                const rootIdx = getNoteIndex(tonic);
                const aNote = getNoteFromIndex((rootIdx + 9) % 12); // 6th degree
                
                noteExamples[0].innerHTML = `e.g., In ${tonic} ${mode}: ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]} &rarr; ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${aNote}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (1-3-6)`;
            }
            else if (romanText.includes("I → iii6")) {
                // I → iii6 (e.g., C-E-G → B-E-G in C Major)
                const rootIdx = getNoteIndex(tonic);
                const bNote = getNoteFromIndex((rootIdx - 1 + 12) % 12); // 7th degree
                
                noteExamples[0].innerHTML = `e.g., In ${tonic} ${mode}: ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]} &rarr; ${bNote}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (7-3-5)`;
            }
            else if (romanText.includes("I → V6/4")) {
                // I → V6/4 (e.g., C-E-G → D-E-G in C Major)
                const rootIdx = getNoteIndex(tonic);
                const dNote = getNoteFromIndex((rootIdx + 2) % 12); // 2nd degree
                
                noteExamples[0].innerHTML = `e.g., In ${tonic} ${mode}: ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]} &rarr; ${dNote}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (2-3-5)`;
            }
            else if (romanText.includes("I → ii")) {
                // I → ii (e.g., C-E-G → D-F-A in C Major)
                const rootIdx = getNoteIndex(tonic);
                const dNote = getNoteFromIndex((rootIdx + 2) % 12); // 2nd degree
                const fNote = getNoteFromIndex((rootIdx + 5) % 12); // 4th degree
                const aNote = getNoteFromIndex((rootIdx + 9) % 12); // 6th degree
                
                noteExamples[0].innerHTML = `e.g., In ${tonic} ${mode}: ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]} &rarr; ${dNote}-${fNote}-${aNote}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (2-4-6)`;
            }
            else if (romanText.includes("I → vii°")) {
                // I → vii° (e.g., C-E-G → B-D-F in C Major)
                const rootIdx = getNoteIndex(tonic);
                const bNote = getNoteFromIndex((rootIdx - 1 + 12) % 12); // 7th degree
                const dNote = getNoteFromIndex((rootIdx + 2) % 12); // 2nd degree
                const fNote = getNoteFromIndex((rootIdx + 5) % 12); // 4th degree
                
                noteExamples[0].innerHTML = `e.g., In ${tonic} ${mode}: ${tonicTriad.notes[0]}-${tonicTriad.notes[1]}-${tonicTriad.notes[2]} &rarr; ${bNote}-${dNote}-${fNote}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (7-2-4)`;
            }
        }
        
        function updateMajorProgressionExamples(stepElement, tonic) {
            const romanDiv = stepElement.querySelector('.roman-numeral');
            if (!romanDiv) return;
            
            // Get scale notes (using Ionian/Major for this progression)
            const scaleNotes = getScaleNotes(tonic, 'Ionian');
            if (scaleNotes.length !== 7) return;
            
            // Get the tonic triad (Major)
            const tonicTriad = getModeSpecificTonicTriad(tonic, 'Ionian');
            if (!tonicTriad || !tonicTriad.notes) return;
            
            const romanText = romanDiv.textContent.trim();
            const noteExamples = stepElement.querySelectorAll('.note-example');
            
            // Map scale indexes to actual note names
            const I = scaleNotes[0]; // Tonic
            const ii = scaleNotes[1]; // 2nd degree
            const iii = scaleNotes[2]; // 3rd degree
            const IV = scaleNotes[3]; // 4th degree
            const V = scaleNotes[4]; // 5th degree
            const vi = scaleNotes[5]; // 6th degree
            const vii = scaleNotes[6]; // 7th degree
            
            if (romanText.includes("Starting point")) {
                // Starting point: I (e.g., C-E-G in C Major)
                noteExamples[0].innerHTML = `Example in ${tonic} Major: ${I}-${iii}-${V}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic} tonic = 1): (1-3-5)`;
            }
            else if (romanText.includes("I → IV")) {
                // I → IV6/4 (e.g., C-E-G → C-F-A in C Major)
                noteExamples[0].innerHTML = `Example in ${tonic} Major: ${I}-${iii}-${V} &rarr; ${I}-${IV}-${vi}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-3-5) &rarr; (1-4-6)`;
                if (noteExamples[2]) {
                    noteExamples[2].innerHTML = `Transformation: Root (${I}) common; 3rd (${iii}&rarr;${IV}) & 5th (${V}&rarr;${vi}) move up one diatonic step.`;
                }
            }
            else if (romanText.includes("IV6/4 → V6")) {
                // IV6/4 → V6 (e.g., C-F-A → B-D-G in C Major)
                noteExamples[0].innerHTML = `Example in ${tonic} Major: ${I}-${IV}-${vi} &rarr; ${vii}-${ii}-${V}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-4-6) &rarr; (7-2-5)`;
                if (noteExamples[2]) {
                    noteExamples[2].innerHTML = `Transformation (example): ${I}&rarr;${vii} (thumb); ${IV}&rarr;${ii} (middle/index); ${vi}&rarr;${V} (pinky/ring). Each voice aims for closest motion.`;
                }
            }
            else if (romanText.includes("V6 → I")) {
                // V6 → I (e.g., B-D-G → C-E-G in C Major)
                noteExamples[0].innerHTML = `Example in ${tonic} Major: ${vii}-${ii}-${V} &rarr; ${I}-${iii}-${V}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (7-2-5) &rarr; (1-3-5)`;
                if (noteExamples[2]) {
                    noteExamples[2].innerHTML = `Transformation: 5th (${V}) common; Bass (${vii}&rarr;${I}) & other voice (${ii}&rarr;${iii}) move up one step.`;
                }
            }
        }

        function updateMinorProgressionExamples(stepElement, tonic) {
            // Use Aeolian (natural minor) mode
            const scaleNotes = getScaleNotes(tonic, 'Aeolian');
            if (scaleNotes.length !== 7) return;
            
            // Special case for harmonic minor: raised 7th
            const rootIdx = getNoteIndex(tonic);
            const leadingTone = getNoteFromIndex((rootIdx + 11) % 12); // Raised 7th
            
            const romanDiv = stepElement.querySelector('.roman-numeral');
            if (!romanDiv) return;
            
            const romanText = romanDiv.textContent.trim();
            const noteExamples = stepElement.querySelectorAll('.note-example');
            
            // Map scale indexes to actual note names
            const i = scaleNotes[0]; // Tonic
            const ii = scaleNotes[1]; // 2nd degree
            const iii = scaleNotes[2]; // 3rd degree (♭3)
            const iv = scaleNotes[3]; // 4th degree
            const v = scaleNotes[4]; // 5th degree
            const vi = scaleNotes[5]; // 6th degree (♭6)
            const vii = scaleNotes[6]; // 7th degree (♭7, but we'll use leading tone where needed)
            
            // Get the tonic triad (minor)
            const tonicTriad = getModeSpecificTonicTriad(tonic, 'Aeolian');
            
            if (romanText.includes("Starting point")) {
                // Starting point: i (e.g., A-C-E in A Minor)
                noteExamples[0].innerHTML = `Example in ${tonic} Minor: ${i}-${iii}-${v}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic} tonic = 1): (1-&flat;3-5)`;
            }
            else if (romanText.includes("i → iv")) {
                // i → iv6/4 (e.g., A-C-E → A-D-F in A Minor)
                noteExamples[0].innerHTML = `Example in ${tonic} Minor: ${i}-${iii}-${v} &rarr; ${i}-${iv}-${vi}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-&flat;3-5) &rarr; (1-4-&flat;6)`;
                if (noteExamples[2]) {
                    noteExamples[2].innerHTML = `Transformation: Root (${i}) common; &flat;3rd (${iii}&rarr;${iv}) & 5th (${v}&rarr;${vi}) of 'i' move up one diatonic step.`;
                }
            }
            else if (romanText.includes("iv6/4 → V6")) {
                // iv6/4 → V6 (e.g., A-D-F → G#-B-E in A Minor)
                // Note: In harmonic minor, V is major with the raised leading tone
                
                // Get the raised 2nd scale degree for V chord's 3rd
                const rootIdx = getNoteIndex(tonic);
                const majorThird = getNoteFromIndex((rootIdx + 4) % 12); // Major 3rd
                
                noteExamples[0].innerHTML = `Example in ${tonic} Minor: ${i}-${iv}-${vi} &rarr; ${leadingTone}-${majorThird}-${v}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (1-4-&flat;6) &rarr; (7-2-5) (Note: ${leadingTone} is the raised 7th)`;
                if (noteExamples[2]) {
                    noteExamples[2].innerHTML = `Transformation: ${i}&rarr;${leadingTone} (raised leading tone); ${iv}&rarr;${majorThird}; ${vi}&rarr;${v}. Each voice aims for closest motion.`;
                }
            }
            else if (romanText.includes("V6 → i")) {
                // V6 → i (e.g., G#-B-E → A-C-E in A Minor)
                const rootIdx = getNoteIndex(tonic);
                const majorThird = getNoteFromIndex((rootIdx + 4) % 12); // Major 3rd
                
                noteExamples[0].innerHTML = `Example in ${tonic} Minor: ${leadingTone}-${majorThird}-${v} &rarr; ${i}-${iii}-${v}`;
                noteExamples[1].innerHTML = `As scale degrees (${tonic}=1): (7-2-5) &rarr; (1-&flat;3-5)`;
                if (noteExamples[2]) {
                    noteExamples[2].innerHTML = `Transformation: 5th (${v}) common; Leading tone (${leadingTone}&rarr;${i}) & other voice (${majorThird}&rarr;${iii}) resolve.`;
                }
            }
        }

        // --- NEW: Update keyboard UI to highlight scale notes ---
        function highlightScaleNotes(tonic, mode) {
            // Get all scale notes for current tonic and mode
            const scaleNotes = getScaleNotes(tonic, mode);
            
            // Reset all keys first
            const allKeys = document.querySelectorAll('.key');
            allKeys.forEach(key => {
                key.classList.remove('scale-note', 'tonic-note');
            });
            
            // Highlight scale notes
            scaleNotes.forEach(note => {
                const keys = document.querySelectorAll(`.key[data-note="${note}"]`);
                keys.forEach(key => {
                    key.classList.add('scale-note');
                });
            });
            
            // Highlight tonic note specially
            const tonicKeys = document.querySelectorAll(`.key[data-note="${tonic}"]`);
            tonicKeys.forEach(key => {
                key.classList.remove('scale-note');
                key.classList.add('tonic-note');
            });
        }

        // --- Event Handlers & Info Update ---
        function handleKeyPress(noteName) {
            currentTonic = noteName;
            updateChordInfo(currentTonic, currentModeName);
            highlightScaleNotes(currentTonic, currentModeName);
            
            // Update transformation examples in the progression section too
            if (currentProgressionTabName) {
                updateTransformationExamples(currentTonic, currentModeName, currentProgressionTabName);
            }
        }

        function updateChordInfo(tonic, mode) {
            tonicNoteSpan.textContent = tonic;
            currentModeDisplaySpan.textContent = mode; 
            const tonicTriadResult = getModeSpecificTonicTriad(tonic, mode);
            if (tonicTriadResult && tonicTriadResult.notes) {
                tonicTriadNotesSpan.textContent = `${tonicTriadResult.notes.join(' - ')} (${tonicTriadResult.quality})`;
            } else {
                tonicTriadNotesSpan.textContent = "N/A";
            }

            diatonicModeKeyTitleSpan.textContent = `${tonic} ${mode}`;
            const diatonicTriads = getDiatonicTriadsForMode(tonic, mode);
            diatonicChordsListDiv.innerHTML = ''; 

            if (diatonicTriads.length > 0) {
                diatonicTriads.forEach(triad => {
                    const card = document.createElement('div');
                    card.classList.add('p-2', 'border', 'rounded', 'bg-white', 'shadow-sm');
                    card.innerHTML = `
                        <p class="font-semibold text-yellow-800">${triad.roman} (${triad.root})</p>
                        <p class="text-xs text-gray-700">${triad.notes.join(' - ')}</p>
                        <p class="text-xs text-gray-500"><em>${triad.quality}</em></p>
                    `;
                    diatonicChordsListDiv.appendChild(card);
                });
            } else {
                diatonicChordsListDiv.innerHTML = '<p class="text-gray-500">Diatonic chords for this mode are not yet fully defined or an error occurred.</p>';
            }
        }

        // --- Initialization ---
        document.addEventListener('DOMContentLoaded', () => {
            createKeyboard();
            // Initialize Mode Tabs with all 7 modes
            createAndHandleTabs(modes, modeSelectorTabsDiv, setModeTabContent, currentModeName, "modeSelector");
            createAndHandleTabs(progressionData, progressionTabsSelectorDiv, setProgressionTabContent, progressionData[0].name, "progressionSelector");
            updateChordInfo(currentTonic, currentModeName);
            highlightScaleNotes(currentTonic, currentModeName);
            
            // Initialize the transformation examples with current tonic
            updateTransformationExamples(currentTonic, currentModeName, progressionData[0].name);
        });
    </script>
</body>
</html>
"""

# Use Streamlit's components.html to render the HTML content
# The height parameter controls how tall the component will be
components.html(html_content, height=1000, scrolling=True)

# Add some additional information below the component
st.markdown("---")
st.markdown("### About this Tool")
st.markdown("""
This interactive music theory visualizer helps you understand various music theory concepts:

- **Explore Different Modes**: Switch between Ionian (Major), Dorian, Phrygian, Lydian, Mixolydian, Aeolian (Minor), and Locrian scales.
- **Visualize Scales**: See which keys belong to each scale with color-coded highlighting.
- **Understand Chord Progressions**: Examine common chord progressions and see how they work in different keys.
- **Study Voice Leading**: Learn how notes move between chords for smooth transitions.

Click on any key on the piano keyboard to set it as the tonic and see how scales and chord progressions work in that key.
""")

st.markdown("---")
st.markdown("Developed with ❤️ for music theory education")

# Run the Streamlit app directly if this script is executed
if __name__ == "__main__":
    pass  # Streamlit already runs the script from top to bottom