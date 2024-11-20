import React, {useState} from 'react';
import Register from './register';
import NoApiKey from './noApiKey';

const Login = ({onLogin}) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showRegister, setShowRegister] = useState(false);
    const [showNoApiKey, setShowNoApiKey] = useState(false);

    const handleLogin = async () => {
        // Here we would send the username, password to the backend for verification
        // Assuming verification is successful, we check if the API key is present
        if (!localStorage.getItem('apiKey')) {
            setShowNoApiKey(true);
        } else {
            onLogin(localStorage.getItem('apiKey'));
        }
    };

    return (<div>
            {showRegister ? (<Register onRegister={() => setShowRegister(false)}/>) : showNoApiKey ? (
                <NoApiKey onAddApiKey={(key) => onLogin(key)} onContinueWithoutApiKey={() => onLogin(null)}/>) : (<div>
                    <h2>Login</h2>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                    />
                    <button onClick={handleLogin}>Login</button>
                    <p>Don't have an account? <button onClick={() => setShowRegister(true)}>Register</button></p>
                </div>)}
        </div>);
};

export default Login;