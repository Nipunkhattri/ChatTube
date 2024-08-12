import React, { useState } from 'react'
import './Register.css'
import { useDispatch, useSelector } from 'react-redux'
import { loginDispatcher, registerDispatcher } from '../redux/features/authSlice'
import { useNavigate } from 'react-router-dom'
import logo from '../assests/yt.png'

const Register = () => {
   const navigate = useNavigate();
   const dispatch = useDispatch();
   const {isAuthenticated} = useSelector(state => state.auth);
   if(isAuthenticated){
    navigate('/');
   }
   const [register,setregister] = useState({
    email:'',
    password:''
   }) 

   const handlechange = (e)=>{
    setregister({...register,[e.target.name]:e.target.value});
   }
   console.log(register);

    const handleLogin = ()=>{
        navigate('/login');
    }

    const handleRegister = async (e) =>{
        e.preventDefault();
        const res = await dispatch(registerDispatcher(register));
        if (res.status == 200){
            navigate('/login');
        }
    }

    return (
    <>
    <div className='call'>
    <div className='logo_container'>
        <img className='logo' src={logo}></img>
        <h4 style={{margin:"0px 0px",fontSize:"20px"}}>Chat with Youtube !</h4>
    </div>
    <div className='register_container'>
        <div className='register_form'>
            <h1>Create Your Account</h1>
            <input type='email' placeholder='Email Address*' className='emailbox' name='email' value={register?.email} onChange={handlechange}/>
            <input type='password' placeholder='Password*' className='emailbox' name='password' value={register?.password} onChange={handlechange}/>
            <button className='btn_submit' onClick={handleRegister}>Register</button>
            <h4 style={{cursor:"pointer"}} onClick={handleLogin}>Already have account ? Login</h4>
            <div className='h_contain'>
            <hr className="h_line"/>
            Or
            <hr className="h_line"/>
            </div>
            <button className='Google_btn'>Continue with Google</button>
        </div>
    </div>
    </div>
    </>
    )
}

export default Register;