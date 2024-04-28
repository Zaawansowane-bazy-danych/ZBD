import { Input, Button } from 'antd';
import 'tailwindcss/tailwind.css';

function WelcomeScreen() {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-8 text-center">Welcome to the Tournament App!</h1>
            <div className="flex flex-col items-center mb-4">
                <Input placeholder="Enter your name" className="w-full md:w-auto text-lg" />
            </div>
            <Button type="primary" className="text-lg h-10">Confirm</Button>
        </div>
    );
}

export default WelcomeScreen;
