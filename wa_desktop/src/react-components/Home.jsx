import React from 'react';

class Home extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="main">
            <div id="home-text">
                <h1 id="home-title">Whats Analysis</h1>
                <p className="body-text" id="first">Whats analysis is a tool to read, process, gather data and create visualizations from whatsapp chats.</p>
            </div>
            </div>
        )
    }
}

export default Home;