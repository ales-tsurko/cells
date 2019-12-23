import React, { useState, useEffect } from 'react';

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
                    <h5>Live Coding Environment</h5>
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
                                snippets and mix different programming languages
                                in the same project.
                            </h5>
                            <Download />
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
                </div>
            </div>
            <Copyright />
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

function Download() {
    const [ selectedOption, setSelectedOption ] = useState();
    const [ options, setOptions ] = useState([]);
    const [ currentRelease, setCurrentRelease ] = useState('');

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
            setCurrentRelease(resp);

            const opts = resp.assets.map((asset) => ({
                value: asset.browser_download_url,
                label: asset.name
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

    return (
        <React.Fragment>
            <Select
                className="download"
                onChange={setSelectedOption}
                options={options}
                placeholder={currentRelease.name}
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
        <div className="copyright">
            &copy; 2019{currentYear > 2019 ? `-${currentYear}` : null}, Ales
            Tsurko
        </div>
    );
}

export default App;
