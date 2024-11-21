// src/App.js

import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Navbar from './components/NavBar';
import Home from './components/Home';
import AnimalList from './components/AnimalList';
import AnimalDetail from './components/AnimalDetail';
import Login from './components/Login';
import Register from './components/Register';
import AccountPage from './components/AccountPage';
import ProtectedRoute from './components/ProtectedRoute';
import AddAnimal from './components/AddAnimal';
import UpdateAnimal from './components/UpdateAnimal';
import UploadCSV from './components/UploadCSV';
import Footer from './components/Footer';

function App() {
    return (
        <Router>
            <Navbar/>
            <div className="container">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/animals" element={<AnimalList/>}/>
                    <Route path="/animals/:id" element={<AnimalDetail/>}/>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/register" element={<Register/>}/>
                    <Route
                        path="/account"
                        element={
                            <ProtectedRoute>
                                <AccountPage/>
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
                        path="/upload-csv"
                        element={
                            <ProtectedRoute>
                                <UploadCSV/>
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
                        path="/upload-csv"
                        element={
                            <ProtectedRoute>
                                <UploadCSV/>
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
