import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import Navbar from './components/NavBar';
import Footer from './components/Footer';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import AddApiKey from './components/AddApiKey';
import AnimalList from './components/AnimalList';
import AnimalDetail from './components/AnimalDetail';
import AddAnimal from './components/AddAnimal';
import UpdateAnimal from './components/UpdateAnimal';
import GenerateDescription from './components/GenerateDescription';
import UploadCSV from './components/UploadCSV';
import ProtectedRoute from './components/ProtectedRoute';
import DeleteAnimal from './components/DeleteAnimal';

function App() {
    return (
        <Router>
            <Navbar/>
            <div className="container">
                <Routes>
                    {/* Public Routes */}
                    <Route path="/" element={<Home/>}/>
                    <Route path="/animals" element={<AnimalList/>}/>
                    <Route path="/animals/:id" element={<AnimalDetail/>}/>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/register" element={<Register/>}/>

                    {/* Protected Routes */}
                    <Route
                        path="/add-api-key"
                        element={
                            <ProtectedRoute>
                                <AddApiKey/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/add-animal"
                        element={
                            <ProtectedRoute>
                                <AddAnimal/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/update-animal/:id"
                        element={
                            <ProtectedRoute>
                                <UpdateAnimal/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/generate-description/:id"
                        element={
                            <ProtectedRoute>
                                <GenerateDescription/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/upload-csv"
                        element={
                            <ProtectedRoute>
                                <UploadCSV/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/delete-animal/:id"
                        element={
                            <ProtectedRoute>
                                <DeleteAnimal/>
                            </ProtectedRoute>
                        }
                    />
                </Routes>
            </div>
            <Footer/>
        </Router>
    );
}

export default App;
