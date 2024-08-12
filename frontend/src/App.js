import logo from './logo.svg';
import './App.css';
import {Routes,Route} from 'react-router-dom'
import Register from './components/Register';
import Login from './components/Login';
import { Home } from './components/Home';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <>
    <ToastContainer />
    <Routes>
      <Route exact path='/register' element={<Register/>}/>
      <Route exact path='/login' element={<Login/>}/>
      <Route exact path='/' element={<Home/>}/>
    </Routes>
    </>
  );
}

export default App;