import { Input, Button } from 'antd';
import 'tailwindcss/tailwind.css';

function WelcomeScreen() {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-8">Welcome to the Tournament App!</h1>
            <div className="flex items-center mb-4">
                <span className="mr-2">Name:</span>
                <Input placeholder="Enter your name" />
            </div>
            <Button type="primary">Confirm</Button>
        </div>
    );
}

export default WelcomeScreen;
