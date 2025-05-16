import streamlit as st
import streamlit.components.v1 as components

# Set page title and configuration
st.set_page_config(
    page_title="Interactive Music Theory Visualizer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# App title and description
st.title("Interactive Music Theory Visualizer")
st.markdown("Explore music theory concepts, scales, and chord progressions with this interactive tool.")

# Define your HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for the piano keyboard */
        .key {
            border: 1px solid #333;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 5px;
            font-weight: bold;
            user-select: none;
            transition: background-color 0.2s;
        }
        .white-key {
            width: 50px;
            height: 200px;
            background-color: white;
            color: black;
            z-index: 1;
        }
        .black-key {
            width: 30px;
            height: 120px;
            background-color: black;
            color: white;
            margin-left: -15px;
            margin-right: -15px;
            z-index: 2;
            position: relative;
        }
        /* Highlighted key styles */
        .key.scale-note {
            box-shadow: 0 0 8px 2px rgba(52, 152, 219, 0.8);
        }
        .white-key.scale-note {
            background-color: #d4e6f1;
        }
        .black-key.scale-note {
            background-color: #2980b9;
        }
        .key.tonic-note {
            box-shadow: 0 0 12px 4px rgba(231, 76, 60, 0.9);
        }
        .white-key.tonic-note {
            background-color: #f9ebea;
        }
        .black-key.tonic-note {
            background-color: #c0392b;
        }
        .keyboard-container {
            display: flex;
            position: relative;
            margin-top: 20px;
            justify-content: center;
            overflow-x: auto;
            padding-bottom: 10px;
            max-width: 100%;
        }
        /* Tab styling */
        .tab {
            padding: 8px 16px;
            cursor: pointer;
            border: 1px solid #d1d5db; /* gray-300 */
            border-bottom: none;
            background-color: #f3f4f6; /* gray-100 */
            margin-right: 2px;
            border-radius: 4px 4px 0 0;
            font-size: 0.875rem; /* text-sm */
        }
        .tab.active {
            background-color: #FFF;
            border-color: #d1d5db; /* gray-300 */
            border-bottom: 1px solid #FFF;
            color: #3b82f6; /* blue-600 */
            font-weight: 600;
        }
        .tab-content-panel {
            border: 1px solid #d1d5db; /* gray-300 */
            padding: 12px;
            border-top: none;
            background-color: #fff;
        }
        .progression-step {
            margin-bottom: 10px; /* Increased spacing */
            padding-bottom: 10px; /* Increased spacing */
            border-bottom: 1px dashed #e5e7eb; /* gray-200 */
        }
        .progression-step:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .progression-step div { /* Add some margin to lines within a step */
            margin-bottom: 2px;
        }
        .roman-numeral { /* Class for Roman numerals */
            color: #059669; /* Tailwind green-700 */
            font-weight: bold;
        }
        .note-example { /* Class for note examples */
            font-style: italic;
            color: #4b5563; /* gray-600 */
        }
        .transformation-desc {  /* Class for transformation descriptions */
             color: #1f2937; /* gray-800 */
        }
    </style>
</head>
<body class="bg-gray-100 p-4 font-sans">

    <div class="container mx-auto max-w-5xl bg-white p-4 rounded-lg shadow-xl">

        <section id="controls" class="mb-4 p-4 bg-gray-50 rounded border relative">
            <div class="flex justify-between items-start">
                <div>
                    <h2 class="text-xl font-semibold text-gray-700 mb-3">Controls</h2>
                    <div id="mode-selector-tabs" class="flex mb-0">
                        </div>
                </div>
                <h1 class="text-lg font-bold text-blue-600 pt-1">Music Theory Visualizer</h1>
            </div>
            <div class="tab-content">
                <p class="text-xs text-gray-500 pt-2">Selected mode influences diatonic relationships.</p>
            </div>
        </section>

        <section id="keyboard-section" class="mb-4 p-4 bg-gray-50 rounded border">
            <h2 class="text-xl font-semibold text-gray-700 mb-2">Piano Keyboard</h2>
            <div id="piano-keyboard" class="keyboard-container">
                </div>
            <p class="text-xs text-gray-500 text-center mt-2">Scroll horizontally to see all keys if needed</p>
        </section>

        <section id="info-display" class="p-4 bg-blue-50 rounded border border-blue-200 mb-4">
            <h2 class="text-xl font-semibold text-gray-700">Information</h2>
            <div id="selected-key-info" class="mt-2 text-lg grid grid-cols-1 md:grid-cols-3 gap-2">
                <p>Selected Tonic: <span id="tonic-note" class="font-semibold text-blue-700">---</span></p>
                <p>Mode: <span id="current-mode-display" class="font-semibold text-blue-700">---</span></p>
                <p>Tonic Triad (I): <span id="tonic-triad-notes" class="font-semibold text-blue-700">---</span></p>
            </div>
        </section> <section id="diatonic-chords-display-container" class="mb-4 p-4 bg-yellow-50 rounded border border-yellow-200">
            <h2 class="text-xl font-semibold text-gray-700 mb-2">Diatonic Triads for <span id="diatonic-mode-key-title" class="text-yellow-700">---</span></h2>
            <div id="diatonic-chords-list" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mt-2 text-sm">
                </div>
        </section>


        <section id="progression-template-section" class="p-4 bg-green-50 rounded border border-green-200">
            <h2 class="text-xl font-semibold text-gray-700 mb-3">Chord Progression Examples & Transformations</h2>
            <div id="progression-tabs-selector" class="flex mb-0">
                </div>
            <div id="progression-tab-content-area">
                </div>
        </section>
    </div>

    <script>
        // --- Music Theory Core ---
        const allNotes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        
        // UPDATED: Added all 7 modes
        const modes = [
            { name: 'Ionian', description: 'Major Scale' },
            { name: 'Dorian', description: 'Minor with raised 6th' },
            { name: 'Phrygian', description: 'Minor with lowered 2nd' },
            { name: 'Lydian', description: 'Major with raised 4th' },
            { name: 'Mixolydian', description: 'Dominant Scale (Major with lowered 7th)' },
            { name: 'Aeolian', description: 'Natural Minor Scale' },
            { name: 'Locrian', description: 'Diminished feel (lowered 2nd, 3rd, 5th, 6th, 7th)' }
        ];
        
        // UPDATED: Added tonic triad intervals for all 7 modes
        const modeIntervals = { // For tonic triad quality
            'Ionian':     { third: 4, fifth: 7, quality: 'Major' },      // R, M3, P5
            'Dorian':     { third: 3, fifth: 7, quality: 'minor' },      // R, m3, P5
            'Phrygian':   { third: 3, fifth: 7, quality: 'minor' },      // R, m3, P5
            'Lydian':     { third: 4, fifth: 7, quality: 'Major' },      // R, M3, P5
            'Mixolydian': { third: 4, fifth: 7, quality: 'Major' },      // R, M3, P5
            'Aeolian':    { third: 3, fifth: 7, quality: 'minor' },      // R, m3, P5
            'Locrian':    { third: 3, fifth: 6, quality: 'diminished' } // R, m3, d5
        };

        // UPDATED: Added scale patterns for all 7 modes (in semitones from the root)
        const scalePatterns = {
            'Ionian':     [0, 2, 4, 5, 7, 9, 11], // W-W-H-W-W-W-H
            'Dorian':     [0, 2, 3, 5, 7, 9, 10], // W-H-W-W-W-H-W
            'Phrygian':   [0, 1, 3, 5, 7, 8, 10], // H-W-W-W-H-W-W
            'Lydian':     [0, 2, 4, 6, 7, 9, 11], // W-W-W-H-W-W-W
            'Mixolydian': [0, 2, 4, 5, 7, 9, 10], // W-W-H-W-W-H-W
            'Aeolian':    [0, 2, 3, 5, 7, 8, 10], // W-H-W-W-H-W-W
            'Locrian':    [0, 1, 3, 5, 6, 8, 10]  // H-W-W-H-W-W-W
        };

        // REMOVED: `modeDiatonicRomanNumerals` as qualities are dynamically determined.
        const romanNumeralStrings = ["I", "II", "III", "IV", "V", "VI", "VII"]; // Used for degree

        let currentTonic = 'C';
        let currentModeName = modes[0].name; // Default to Ionian
        let currentProgressionTabName = null; // To track selected progression

        function getNoteIndex(note) { return allNotes.indexOf(note); }
        function getNoteFromIndex(index) { return allNotes[index % 12]; }

        function getModeSpecificTonicTriad(rootNote, modeName) {
            const rootIndex = getNoteIndex(rootNote);
            if (rootIndex === -1) return null;
            
            const intervals = modeIntervals[modeName];
            if (!intervals) { // Fallback if mode somehow not in modeIntervals
                console.warn(`Tonic intervals for mode '${modeName}' not defined. Using Ionian.`);
                const ionianIntervals = modeIntervals['Ionian'];
                const thirdNoteFallback = getNoteFromIndex(rootIndex + ionianIntervals.third);
                const fifthNoteFallback = getNoteFromIndex(rootIndex + ionianIntervals.fifth);
                return {
                    notes: [rootNote, thirdNoteFallback, fifthNoteFallback],
                    quality: ionianIntervals.quality
                };
            }

            const thirdNote = getNoteFromIndex(rootIndex + intervals.third);
            const fifthNote = getNoteFromIndex(rootIndex + intervals.fifth);
            return {
                notes: [rootNote, thirdNote, fifthNote],
                quality: intervals.quality
            };
        }

        function getScaleNotes(rootNote, modeName) {
            const rootIndex = getNoteIndex(rootNote);
            if (rootIndex === -1) return [];
            
            const pattern = scalePatterns[modeName];
            if (!pattern) {
                console.warn(`Scale pattern for mode '${modeName}' not defined. Returning empty scale.`);
                return [];
            }
            return pattern.map(interval => getNoteFromIndex(rootIndex + interval));
        }

        function getTriadQuality(root, third, fifth) {
            const rootIdx = getNoteIndex(root);
            if (rootIdx === -1) return "Unknown";
            let thirdIdx = getNoteIndex(third);
            if (thirdIdx === -1) return "Unknown";
            let fifthIdx = getNoteIndex(fifth);
            if (fifthIdx === -1) return "Unknown";

            // Normalize indices to be relative to root for interval calculation
            if (thirdIdx < rootIdx) thirdIdx += 12;
            if (fifthIdx < rootIdx) fifthIdx += 12;
            // Second adjustment for fifth if third wrapped but fifth didn't yet need to pass third
            if (fifthIdx < thirdIdx && thirdIdx > rootIdx) fifthIdx += 12;


            const intervalToThird = thirdIdx - rootIdx;
            const intervalToFifth = fifthIdx - rootIdx;

            if (intervalToThird === 4 && intervalToFifth === 7) return "Major";
            if (intervalToThird === 3 && intervalToFifth === 7) return "minor";
            if (intervalToThird === 3 && intervalToFifth === 6) return "diminished";
            if (intervalToThird === 4 && intervalToFifth === 8) return "augmented"; // Not common in diatonic modes
            return "Unknown";
        }
        
        function getDiatonicTriadsForMode(rootNote, modeName) {
            const scale = getScaleNotes(rootNote, modeName);
            if (scale.length !== 7) return [];

            const triads = [];
            for (let i = 0; i < 7; i++) {
                const triadRoot = scale[i];
                const triadThird = scale[(i + 2) % 7]; 
                const triadFifth = scale[(i + 4) % 7];
                
                const quality = getTriadQuality(triadRoot, triadThird, triadFifth);
                
                let roman = romanNumeralStrings[i];
                if (quality === "minor" || quality === "diminished" || quality === "augmented") { // Augmented minor? no.
                    roman = roman.toLowerCase();
                }
                if (quality === "diminished") roman += "°";
                if (quality === "augmented") roman += "+";

                triads.push({
                    degree: i + 1,
                    roman: roman,
                    root: triadRoot,
                    notes: [triadRoot, triadThird, triadFifth],
                    quality: quality
                });
            }
            return triads;
        }

        // --- UI Elements (unchanged) ---
        const pianoKeyboardDiv = document.getElementById('piano-keyboard');
        const tonicNoteSpan = document.getElementById('tonic-note');
        const currentModeDisplaySpan = document.getElementById('current-mode-display');
        const tonicTriadNotesSpan = document.getElementById('tonic-triad-notes');
        const modeSelectorTabsDiv = document.getElementById('mode-selector-tabs');
        const progressionTabsSelectorDiv = document.getElementById('progression-tabs-selector');
        const progressionTabContentAreaDiv = document.getElementById('progression-tab-content-area');
        const diatonicModeKeyTitleSpan = document.getElementById('diatonic-mode-key-title');
        const diatonicChordsListDiv = document.getElementById('diatonic-chords-list');

        // --- Keyboard Generation with 2 octaves ---
        const keyboardLayout = [
            // First octave
            { name: 'C', type: 'white', displayName: 'C' }, { name: 'C#', type: 'black', displayName: 'C#' },
            { name: 'D', type: 'white', displayName: 'D' }, { name: 'D#', type: 'black', displayName: 'D#' },
            { name: 'E', type: 'white', displayName: 'E' },
            { name: 'F', type: 'white', displayName: 'F' }, { name: 'F#', type: 'black', displayName: 'F#' },
            { name: 'G', type: 'white', displayName: 'G' }, { name: 'G#', type: 'black', displayName: 'G#' },
            { name: 'A', type: 'white', displayName: 'A' }, { name: 'A#', type: 'black', displayName: 'A#' },
            { name: 'B', type: 'white', displayName: 'B' },
            // Second octave
            { name: 'C2', type: 'white', displayName: 'C' }, { name: 'C#2', type: 'black', displayName: 'C#' },
            { name: 'D2', type: 'white', displayName: 'D' }, { name: 'D#2', type: 'black', displayName: 'D#' },
            { name: 'E2', type: 'white', displayName: 'E' },
            { name: 'F2', type: 'white', displayName: 'F' }, { name: 'F#2', type: 'black', displayName: 'F#' },
            { name: 'G2', type: 'white', displayName: 'G' }, { name: 'G#2', type: 'black', displayName: 'G#' },
            { name: 'A2', type: 'white', displayName: 'A' }, { name: 'A#2', type: 'black', displayName: 'A#' },
            { name: 'B2', type: 'white', displayName: 'B' },
            { name: 'C3', type: 'white', displayName: 'C' }
        ];
        function createKeyboard() {
            pianoKeyboardDiv.innerHTML = '';
            keyboardLayout.forEach((keyData) => {
                const keyElement = document.createElement('div');
                keyElement.classList.add('key');
                keyElement.textContent = keyData.displayName;
                
                // Extract the base note name without octave number
                const baseName = keyData.name.replace(/[0-9]/g, '');
                keyElement.dataset.note = baseName;
                
                keyElement.classList.add(keyData.type === 'white' ? 'white-key' : 'black-key');
                keyElement.addEventListener('click', () => handleKeyPress(keyElement.dataset.note));
                pianoKeyboardDiv.appendChild(keyElement);
            });
        }

        // --- Generic Tab Handling Logic (unchanged) ---
        function createAndHandleTabs(tabsArray, tabsContainerDiv, contentSetterFunction, initialTabName, instanceName) {
            let currentActiveTabName = initialTabName;
            tabsContainerDiv.innerHTML = ''; 

            tabsArray.forEach((tabData) => {
                const tabElement = document.createElement('div');
                tabElement.classList.add('tab');
                tabElement.textContent = tabData.name;
                tabElement.dataset.tabName = tabData.name;
                if (tabData.name === currentActiveTabName) {
                    tabElement.classList.add('active');
                }
                tabElement.addEventListener('click', () => {
                    currentActiveTabName = tabData.name;
                    if (instanceName === "modeSelector") { 
                         currentModeName = tabData.name; 
                         updateChordInfo(currentTonic, currentModeName); 
                         highlightScaleNotes(currentTonic, currentModeName);
                    } else if (instanceName === "progressionSelector") {
                        currentProgressionTabName = tabData.name;
                    }
                    updateActiveStatus(tabsContainerDiv, currentActiveTabName);
                    contentSetterFunction(tabData.name); 
                    
                    // If a progression tab is clicked, update transformation examples
                    if (instanceName === "progressionSelector") {
                        updateTransformationExamples(currentTonic, currentModeName, tabData.name);
                    }
                });
                tabsContainerDiv.appendChild(tabElement);
            });
            if (tabsArray.length > 0) {
                if (instanceName === "progressionSelector") {
                    currentProgressionTabName = initialTabName;
                }
                contentSetterFunction(currentActiveTabName); 
            }
        }

        function updateActiveStatus(tabsContainerDiv, activeTabName) {
            const tabs = tabsContainerDiv.querySelectorAll('.tab');
            tabs.forEach(tab => {
                if (tab.dataset.tabName === activeTabName) {
                    tab.classList.add('active');
                } else {
                    tab.classList.remove('active');
                }
            });
        }
        
        // --- Content Setters for Tabs (progressionData content is unchanged) ---
        function setModeTabContent(modeName) { /* No specific content for mode tabs themselves */ }
        const progressionData = [ // Unchanged from V0.4
            {
                name: "Generic I Moves",
                id: "generic-i",
                content: `
                    <p class="text-sm text-gray-600 mb-3">Common minimal voice-leading moves from a generic Root Position <span class="roman-numeral">I</span> chord.</p>
                    <ul class="list-disc list-inside space-y-1 text-sm">
                        <li class="progression-step"><div><span class="roman-numeral">I &rarr; V<sup>6</sup></span></div><div class="note-example">e.g., In C Major: C-E-G &rarr; B-D-G</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (7-2-5)</div><div class="transformation-desc">Transformation: Root & 3rd move down one diatonic step, 5th common.</div></li>
                        <li class="progression-step"><div><span class="roman-numeral">I &rarr; IV<sup>6/4</sup></span></div><div class="note-example">e.g., In C Major: C-E-G &rarr; C-F-A</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (1-4-6)</div><div class="transformation-desc">Transformation: Root common; 3rd & 5th move up one diatonic step.</div></li>
                        <li class="progression-step"><div><span class="roman-numeral">I &rarr; vi<sup>6</sup></span> (Am/C from C)</div><div class="note-example">e.g., In C Major: C-E-G &rarr; C-E-A</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (1-3-6)</div><div class="transformation-desc">Transformation: Root & 3rd common, 5th moves to 6th (of Root).</div></li>
                        <li class="progression-step"><div><span class="roman-numeral">I &rarr; iii<sup>6</sup></span> (Em/B from C)</div><div class="note-example">e.g., In C Major: C-E-G &rarr; B-E-G</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (7-3-5)</div><div class="transformation-desc">Transformation: 3rd & 5th common, Root moves down one diatonic step.</div></li>
                        <li class="progression-step"><div><span class="roman-numeral">I &rarr; V<sup>6/4</sup></span> (G/D from C)</div><div class="note-example">e.g., In C Major: C-E-G &rarr; D-E-G</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (2-3-5)</div><div class="transformation-desc">Transformation: 3rd & 5th common, Root moves up one diatonic step.</div></li>
                        <li class="progression-step"><div><span class="roman-numeral">I &rarr; ii</span></div><div class="note-example">e.g., In C Major: C-E-G &rarr; D-F-A</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (2-4-6)</div><div class="transformation-desc">Transformation: All three notes move UP one diatonic step.</div></li>
                        <li class="progression-step"><div><span class="roman-numeral">I &rarr; vii°</span></div><div class="note-example">e.g., In C Major: C-E-G &rarr; B-D-F</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (7-2-4)</div><div class="transformation-desc">Transformation: All three notes move DOWN one diatonic step.</div></li>
                    </ul>`
            },
            {
                name: "I-IV-V-I (Major)",
                id: "i-iv-v-i-maj",
                content: `
                    <p class="text-sm text-gray-600 mb-3">Progression example. Voice leading aims for smoothness, often using inversions.</p>
                    <div class="text-sm space-y-2">
                        <div class="progression-step"><div>Starting point: <span class="roman-numeral">I</span></div><div class="note-example">Example in C Major: C-E-G</div><div class="note-example">As scale degrees (C tonic = 1): (1-3-5)</div></div>
                        <div class="progression-step"><div><span class="roman-numeral">I &rarr; IV<sup>6/4</sup></span></div><div class="note-example">Example in C Major: C-E-G &rarr; C-F-A</div><div class="note-example">As scale degrees (C=1): (1-3-5) &rarr; (1-4-6)</div><div class="transformation-desc">Transformation: Root (C) common; 3rd (E&rarr;F) & 5th (G&rarr;A) move up one diatonic step.</div></div>
                        <div class="progression-step"><div><span class="roman-numeral">IV<sup>6/4</sup> &rarr; V<sup>6</sup></span></div><div class="note-example">Example in C Major: C-F-A &rarr; B-D-G</div><div class="note-example">As scale degrees (C=1): (1-4-6) &rarr; (7-2-5)</div><div class="transformation-desc">Transformation (example): C&rarr;B (thumb); F&rarr;D (middle/index); A&rarr;G (pinky/ring). Each voice aims for closest motion.</div></div>
                        <div class="progression-step"><div><span class="roman-numeral">V<sup>6</sup> &rarr; I</span></div><div class="note-example">Example in C Major: B-D-G &rarr; C-E-G</div><div class="note-example">As scale degrees (C=1): (7-2-5) &rarr; (1-3-5)</div><div class="transformation-desc">Transformation: 5th (G) common; Bass (B&rarr;C) & other voice (D&rarr;E) move up one step.</div></div>
                    </div>`
            },
            {
                name: "i-iv-V-i (Minor)",
                id: "i-iv-v-i-min",
                content: `
                    <p class="text-sm text-gray-600 mb-3">Progression example using harmonic minor for a Major V. Voice leading aims for smoothness.</p>
                    <div class="text-sm space-y-2">
                        <div class="progression-step"><div>Starting point: <span class="roman-numeral">i</span></div><div class="note-example">Example in A Minor: A-C-E</div><div class="note-example">As scale degrees (A tonic = 1): (1-&flat;3-5)</div></div>
                        <div class="progression-step"><div><span class="roman-numeral">i &rarr; iv<sup>6/4</sup></span> (Dm/A)</div><div class="note-example">Example in A Minor: A-C-E &rarr; A-D-F</div><div class="note-example">As scale degrees (A=1): (1-&flat;3-5) &rarr; (1-4-&flat;6)</div><div class="transformation-desc">Transformation: Root (A) common; &flat;3rd (C&rarr;D) & 5th (E&rarr;F) of 'i' move up one diatonic step.</div></div>
                        <div class="progression-step"><div><span class="roman-numeral">iv<sup>6/4</sup> &rarr; V<sup>6</sup></span> (E/G# - V is E Major)</div><div class="note-example">Example in A Minor: A-D-F &rarr; G#-B-E</div><div class="note-example">As scale degrees (A=1): (1-4-&flat;6) &rarr; (7-2-5) (Note: G# is the raised 7th)</div><div class="transformation-desc">Transformation: A&rarr;G# (raised leading tone); D&rarr;B; F&rarr;E. Each voice aims for closest motion.</div></div>
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