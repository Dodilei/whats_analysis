import React from 'react';

import make_page from './page';

class Header extends React.Component {

    constructor(props) {
        super(props);
        this.highlight = {
            home: false,
            setup: false,
            info: false,
            graphs: false
        }
        this.highlight[props.highlight] = true;

        this.state = {
            Page: make_page('home'),
        };

        this.changePage = this.changePage.bind(this);
    }

    changePage(e, identifier) {
        return null
    }

    render() {
        return (
            [<div id="header">
                <a id="logo" href="#" onClick={this.changePage('home')}>Whats Analysis
                </a>
                <nav id="navbar">
                    <a class="nav-button" href="#" onClick={this.changePage('home')} id="nav-setup">Setup
                    <span id={this.highlight["setup"] ? "highlight" : "no-highlight"}></span>
                    </a>
                    <a class="nav-button" href="#" onClick={this.changePage('home')} id="nav-info">Info
                    <span id={this.highlight["info"] ? "highlight" : "no-highlight"}></span>
                    </a>
                    <a class="nav-button" href="#" onClick={this.changePage('home')} id="nav-graph">Graph
                    <span id={this.highlight["graphs"] ? "highlight" : "no-highlight"}></span>
                    </a>
                </nav>
                <button id="settings-button">
                <object id="settings-object" data="assets/settings-icon.svg" type="image/svg+xml" aria-label="settings"></object>
                </button>
            </div>,
            <this.state.Page />]
        )
    }
}

export default Header;