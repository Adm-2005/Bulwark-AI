import { useState, useEffect } from "react";
import NetworkCard from "../components/NetworkCard";

const NetworkList = () => {
    const colors = ['primary', 'secondary', 'accent']
    const [networks, setNetworks] = useState([]);

    return (
        <section className="flex flex-col gap-4 w-full items-center p-7">
            <h1 className="text-gray-400 text-center font-poppins font-bold text-3xl">Your Networks</h1>
            
            <div className="flex flex-col w-full items-center justify-center gap-2">
                {networks.map((network, index) => {
                    const color = colors[index % colors.length] 

                    return (<NetworkCard network={network} color={color} />)
                })}
            </div>
            <button className="bg-red-700 hover:bg-red-900 py-[8px] px-[18px] rounded-lg text-white font-poppins font-semibold">Add Network +</button>
        </section>
    )
}

export default NetworkList;