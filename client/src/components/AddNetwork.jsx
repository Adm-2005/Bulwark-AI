import { useState } from 'react';

const AddNetwork = ({ networks, setNetworks, addNetworkOpen, setAddNetworkOpen }) => {
    const [ connectionMethod, setConnectionMethod ] = useState('SSH')

    const handleMethodChange = (e) => {
        setConnectionMethod(e.target.value);
    }

    const handleFormSubmit = (e) => {
        const newNetwork = {}
        setNetworks((prev) => [...prev, newNetwork])
        setAddNetworkOpen(false)
    }

    return (
        <div className="bg-gradient-to-r from-[#142462] to-[#030A10] z-10 flex flex-col justify-center items-center w-1/2 h-[500px] absolute left-[25%] top-[20%] rounded-lg border border-primary">
            <form 
                onSubmit={handleFormSubmit}
                className="flex flex-col gap-4 items-center justify-center h-full w-full"
            >
                <div className="flex flex-col font-poppins w-3/5 justify-center">
                    <label className="text-primary text-lg">Name*</label>
                    <input 
                        type="text"
                        className="bg-gray-300 p-2 rounded-lg w-full focus:outline-none focus:border-2 border-primary text-primary"
                    ></input>
                </div>

                <div className="flex flex-col font-poppins w-3/5 justify-center">
                    <label className="text-primary text-lg">IP Address*</label>
                    <input 
                        type="text"
                        className="bg-gray-300 p-2 rounded-lg w-full focus:outline-none focus:border-2 border-primary text-primary"
                    ></input>
                </div>

                <div className="flex flex-col font-poppins w-3/5 justify-center">
                    <label className="text-primary text-lg">Connection Method*</label>
                    <select
                        onChange={handleMethodChange} 
                        value={connectionMethod}
                        className='bg-gray-300 p-2 rounded-lg w-full focus:outline-none focus:border-2 border-primary text-primary'
                    >
                        <option value={'SSH'}>
                            SSH
                        </option>
                        <option value={'API'}>
                            API
                        </option>
                    </select>
                </div>

                {connectionMethod === 'SSH' 
                    ? (
                        <div className="flex flex-col font-poppins w-3/5 justify-center">
                            <label className="text-primary text-lg">SSH Key</label>
                            <input 
                                type="text"
                                className="bg-gray-300 p-2 rounded-lg w-full focus:outline-none focus:border-2 border-primary text-primary"
                            ></input>
                        </div>
                    )
                    : (
                        <div className="flex flex-col font-poppins w-3/5 justify-center">
                            <label className="text-primary text-lg">API Token</label>
                            <input 
                                type="text"
                                className="bg-gray-300 p-2 rounded-lg w-full focus:outline-none focus:border-2 border-primary text-primary"
                            ></input>
                        </div>
                    )
                }

                <button 
                    className="bg-gradient-to-r from-[#ffae52] to-[#E3436B] hover:bg-[#E3436B] cursor-pointer mt-5 text-lg text-white font-poppins font-medium py-[8px] px-[18px] rounded-full shadow-xl"
                >
                    Submit
                </button>
            </form>
        </div>
    )
}

export default AddNetwork;