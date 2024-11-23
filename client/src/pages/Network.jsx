import { useState, useEffect } from "react";
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import NetworkList from "../sections/NetworksList";

const Network = () => {
    return (
        <div className="bg-gradient-to-r from-[#142462] to-[#030A10] w-full flex flex-col min-h-screen">
            <Navbar />

            <NetworkList />

            <Footer />
        </div>
    )
}

export default Network;