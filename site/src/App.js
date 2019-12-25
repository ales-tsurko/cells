import React, { useState, useEffect } from 'react';

import anime from 'animejs/lib/anime.es.js';
import GitHubButton from 'react-github-btn';
import Select from 'react-select';

import './app.scss';
import languages from './images/languages.jpg';

function App() {
    return (
        <div className="main">
            <Cells />
            <div className="content">
                <div className="content-row header">
                    <h1>Cells</h1>
                    <Subtitle />
                </div>

                <div className="content-row middle">
                    <div className="content-description video">
                        <iframe
                            title="cells-video"
                            width="570"
                            height="323"
                            src="https://www.youtube.com/embed/S0QfVc6bMhg"
                            frameBorder="0"
                            allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                        />
                    </div>

                    <div className="content-description">
                        <div className="description-container">
                            <h5>
                                Cells allows you to organize code into runnable
                                snippets and mix programming languages.
                            </h5>
                            <div
                                style={{
                                    display: 'flex',
                                    justifyContent: 'flex-start',
                                    alignItems: 'center'
                                }}
                            >
                                <Download />
                                <div style={{ marginLeft: 28 }}>
                                    <GitHubButton
                                        href="https://github.com/AlesTsurko/cells"
                                        data-size="large"
                                        data-show-count="true"
                                        aria-label="Star AlesTsurko/cells on GitHub"
                                        style={{ display: 'inline-block' }}
                                    >
                                        Star
                                    </GitHubButton>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="content-row bottom">
                    <div className="content-description">
                        <div
                            style={{
                                backgroundImage: `url("${languages}")`,
                                width: 383,
                                height: 186
                            }}
                        />
                    </div>
                    <div className="content-description copy">
                        <Copyright />
                    </div>
                </div>
            </div>
        </div>
    );
}

function Cells() {
    return (
        <div className="cells">
            <div>
                <div className="cell-1" />
            </div>
            <div>
                <div className="cell-2" />
            </div>
            <div>
                <div className="cell-3" />
            </div>
        </div>
    );
}

function Subtitle() {
    const [ subtitle, setSubtitle ] = useState([
        'Live',
        'Coding',
        'Environment'
    ]);
    const words = [
        [ 'Live', 'Generative', 'Algorithmic', 'Creative' ],
        [
            'Coding',
            'Prototyping',
            'Audio',
            'Visuals',
            'Thing',
            'Music',
            'Arts'
        ],
        [ 'Environment', 'Workstation', 'Sequencer', 'Editor' ]
    ];

    const updateSubtitle = () => {
        const wordPosition = Math.round(Math.random() * (words.length - 1));
        const index = Math.round(
            Math.random() * (words[wordPosition].length - 1)
        );

        let transition = subtitle[wordPosition];

        anime({
            duration: 4000,
            easing: 'easeInOutCirc',
            update: () => {
                transition = interpolateString(
                    transition,
                    words[wordPosition][index]
                );
                let nextSubtitle = [ ...subtitle ];
                nextSubtitle[wordPosition] = transition;
                setSubtitle(nextSubtitle);
            }
        }).finished.then(updateSubtitle);
    };

    useEffect(() => {
        setTimeout(updateSubtitle, 3000);
    }, []);

    return <h5>{`${subtitle[0]} ${subtitle[1]} ${subtitle[2]}`}</h5>;
}

function interpolateString(from, to) {
    if (from === to) return from;

    let result = '';

    for (let n = 0; n < from.length; n++) {
        if (n > to.length - 1) return result;
        result += interpolateChar(from.charAt(n), to.charAt(n));
    }

    for (let n = from.length; n < to.length; n++) {
        result += interpolateChar(' ', to.charAt(n));
    }

    return result;
}

function interpolateChar(char, to) {
    if (char === to) return to;
    const code = char < to ? char.charCodeAt(0) + 1 : char.charCodeAt(0) - 1;

    return String.fromCharCode(code);
}

function Download() {
    const [ selectedOption, setSelectedOption ] = useState();
    const [ options, setOptions ] = useState([]);
    const styles = {
        option: (provided, state) => ({
            ...provided,
            color: state.isFocused ? '#ffffff' : '#000000',
            backgroundColor: state.isFocused ? '#5b00c3' : '#ffffff',
            padding: 20
        }),
        placeholder: (provided, state) => ({
            color: '#000000'
        }),
        singleValue: (provided, state) => {
            const opacity = state.isDisabled ? 0.5 : 1;
            const transition = 'opacity 300ms';

            return { ...provided, opacity, transition };
        }
    };

    useEffect(() => {
        async function fetchData() {
            const resp = await fetch(
                'https://api.github.com/repos/AlesTsurko/cells/releases/latest'
            );

            if (resp.ok) {
                const res = await resp.json();
                return res;
            }
        }

        fetchData().then(handleResponse);
    }, []);

    function handleResponse(resp) {
        if (resp) {
            const opts = resp.assets.map((asset) => ({
                value: asset.browser_download_url,
                label: resp.tag_name,
                name: asset.name
            }));

            setOptions(opts);
        }
    }

    useEffect(
        () => {
            if (selectedOption) {
                document.getElementById('download-link').click();
            }
        },
        [ selectedOption ]
    );

    function getLabel({ label, name }) {
        return (
            <div className="download-option">
                <span style={{ fontWeight: 600 }}>
                    {name.indexOf('.deb.') > 0 ? 'Linux | 64 bit' : 'macOS'}
                </span>
                <span>{label}</span>
                <span style={{ fontSize: 14, opacity: 0.7 }}>{name}</span>
            </div>
        );
    }

    return (
        <React.Fragment>
            <Select
                formatOptionLabel={getLabel}
                styles={styles}
                className="download-container"
                classNamePrefix="download-select"
                onChange={setSelectedOption}
                options={options}
                placeholder="Download"
                isSearchable={false}
            />
            {selectedOption && (
                <a
                    id="download-link"
                    href={selectedOption.value}
                    download
                    style={{ display: 'none' }}
                >
                    Download
                </a>
            )}
        </React.Fragment>
    );
}

function Copyright() {
    const [ currentYear ] = useState(new Date().getFullYear());

    return (
        <span className="copyright">
            &copy; 2019{currentYear > 2019 ? `-${currentYear}` : null}, Ales
            Tsurko.
        </span>
    );
}

export default App;
