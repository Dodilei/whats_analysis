import React from 'react';

class Setup extends React.Component {

    constructor(props) {
        super(props);

        this.changeVisible = this.changeVisible.bind(this);

        this.state = {
            visible: "guide"
        };

        this.guideHTML = (
            <div id="main">
            <div id="setup-text">
                <h1 id="setup-title" className="title">Setup</h1>
                <h2 id="setup-prerequisites">- Prerequisites</h2>
                <p className="setup-body-text body-text" id="setup-first">Some manual arrangements can improve code functionality and the readability of the data display:
                    <br/><br/>
                    <ul id="setup-prereq-list">
                        <li>Place an empty newline in the beginning and end of each chat (if it doesn't exist yet)</li>
                        <li>Merge chats with the same person (especially when someone changes their phone number, don't forget to update all the names inside de text file)</li>
                        <li>Use clean, readable names (if a change is made, both the file name and all the entries in the text must be updated)</li>
                        <li>Do not include chats with less than two messages (why would you??)
                        </li>
                        <li>When exporting the chats, do not export media (it's not supported, yet)</li>
                    </ul>
                </p>
            </div>
            <div id="setup-button-container">
                <button id="setup-button" onClick={this.changeVisible}>
                    Start Import
                </button>
            </div>
            </div>
        );

        this.importHTML = (
            <p>soon</p>
        )

        this.modes = {
            guide: this.guideHTML,
            import: this.importHTML
        };
    };

    changeVisible() {
        if (this.state.visible === "guide") {
            this.setState(
                { visible: "import" }
            );
        } else {
            this.setState(
                { visible: "guide" }
            );
        };
    };

    render() {
        return (
            this.modes[this.state.visible]
        )
    }
}

export default Setup;