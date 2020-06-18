import React from 'react';

class Home extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="main">
            <div id="text">
                <h1 id="title">Whats Analysis</h1>
                <p class="body_text" id="first">Whats analysis is a tool to read, process, gather data and create visualizations from whatsapp chats.</p>
            </div>
            </div>
        )
    }
}

export default Home;