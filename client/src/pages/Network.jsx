import { useState, useEffect } from "react";
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import NetworkList from "../sections/NetworksList";
import AddNetwork from "../components/AddNetwork";

const Network = () => {
    const [addNetworkOpen, setAddNetworkOpen] = useState(false);
    const [networks, setNetworks] = useState([]);

    return (
        <div className="bg-gradient-to-r from-[#142462] to-[#030A10] w-full flex flex-col min-h-screen">
            <Navbar />

            {addNetworkOpen && (
                <AddNetwork 
                    networks={networks} 
                    setNetworks={setNetworks} 
                    addNetworkOpen={addNetworkOpen} 
                    setAddNetworkOpen={setAddNetworkOpen} 
                />
            )}

            <NetworkList 
                networks={networks} 
                addNetworkOpen={addNetworkOpen} 
                setAddNetworkOpen={setAddNetworkOpen} 
            />

            <Footer />
        </div>
    )
}

export default Network;