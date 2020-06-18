import Home from './Home.jsx'
import Setup from './Setup.jsx'
import Info from './Info.jsx'
import Graphs from './Graphs.jsx'

function make_page(identifier) {

    const pages = {
        home: Home,
        info: Info,
        setup: Setup,
        graphs: Graphs
    };

    return pages[identifier];
}

export default make_page;