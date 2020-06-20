import React from 'react';

import make_page from './page';

class Header extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            current_page: props.startPage,
            Page: make_page(props.startPage),
        };

        this.changePage = this.changePage.bind(this);
    };

    changePage(e) {
        let target = e.currentTarget.getAttribute("href").slice(1);
        this.setState({
            current_page: target,
            Page: make_page(target)
        });
    };

    setHighlight(identifier) {
        if (this.state.current_page === identifier) {
            return "highlight-span";
        };
    };

    render() {
        return (
            [<div id="header">
                <a id="logo" href="#home" onClick={this.changePage}>Whats Analysis
                </a>
                <nav id="navbar">
                    <a className="nav-button" href="#setup" onClick={this.changePage} id="nav-setup">Setup
                    <span id={this.setHighlight("setup")}></span>
                    </a>
                    <a className="nav-button" href="#info" onClick={this.changePage} id="nav-info">Info
                    <span id={this.setHighlight("info")}></span>
                    </a>
                    <a className="nav-button" href="#graphs" onClick={this.changePage} id="nav-graph">Graphs
                    <span id={this.setHighlight("graphs")}></span>
                    </a>
                </nav>
                <button id="settings-button">
                <object id="settings-object" data="assets/settings-icon.svg" type="image/svg+xml" aria-label="settings"></object>
                </button>
            </div>,
            <this.state.Page />]
        );
    };
};

export default Header;