import React,{useState} from 'react'
import './Register.css'
import logo from '../assests/yt.png'
import { useDispatch, useSelector } from 'react-redux'
import { loginDispatcher } from '../redux/features/authSlice'
import { useNavigate } from 'react-router-dom'
const Login = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const {isAuthenticated} = useSelector(state => state.auth);
    if(isAuthenticated){
     navigate('/');
    }
    const [login,setlogin] = useState({
     email:'',
     password:''
    }) 
    const handlechange = (e)=>{
     setlogin({...login,[e.target.name]:e.target.value});
    }

    const handleLogin = async (e) =>{
        e.preventDefault();
        const res = await dispatch(loginDispatcher(login));
        console.log(res);
        if (res.status == 200){
            navigate('/');
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
            <h1>Welcome You !</h1>
            <input type='email' placeholder='Email Address*' className='emailbox' name='email' value={login?.email} onChange={handlechange}/>
            <input type='password' placeholder='Password*' className='emailbox' name='password' value={login?.password} onChange={handlechange}/>
            <button className='btn_submit' onClick={handleLogin}>Login</button>
            <h4>Don't have an account ? Register</h4>
            <div className='h_contain'>
            <hr className="h_line"/>
            Or
            <hr className="h_line"/>
            </div>
            <button className='Google_btn'>Continue with Google</button>
        </div>
    </div>
    </div>
    </>  )
}
export default Login;