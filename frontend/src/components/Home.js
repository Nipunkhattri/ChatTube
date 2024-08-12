import React, { useEffect, useState } from 'react'
import './Home.css'
import { FaToggleOff } from "react-icons/fa6";
import logo from '../assests/yt.png'
import { HiMiniPencilSquare } from "react-icons/hi2";
import { FaRegLightbulb } from "react-icons/fa";
import { IoCodeSlash } from "react-icons/io5";
import { LiaHandsHelpingSolid } from "react-icons/lia";
import { IoIosSend } from "react-icons/io";
import { IoMdClose } from "react-icons/io";
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { CheckProcess, Process_video, SaveId, SendQuery, getHistory, getallIds } from '../redux/features/authSlice';
import { toast } from 'react-toastify';
import user from '../assests/user.png';
import ai from '../assests/ai.png';
export const Home = () => {
  const [open, setopen] = useState(false);
  const [load, setload] = useState(false);
  const [container, setcontainer] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { isAuthenticated } = useSelector(state => state.auth);

  if (!isAuthenticated) {
    navigate('/login');
  }
  const { Ids } = useSelector(state => state.auth)
  const [videolink, setvideolink] = useState({
    Youtube_link: ""
  })
  const [loader,setloader] = useState(false);
  const { chat } = useSelector(state => state.auth);
  const { id } = useSelector(state => state.auth);

  // Get chat history 
  const getChatHistory = () => {
    if (id != null)
      dispatch(getHistory(id));
  }

  useEffect(() => {
    getChatHistory();
  }, [id])

  const [Askquery, setAskquery] = useState({
    id: id,
    query: ""
  })

  useEffect(() => {
    if(chat != null){
      if (chat.length > 0) {
        setcontainer(true);
      }
    }
  }, [chat])

  console.log(Askquery);

  const send = async (e) => {
    e.preventDefault();
    setloader(true);
    setcontainer(true);
    const res = await dispatch(SendQuery(Askquery));
    if (res.status == 200) {
      getChatHistory()
      setloader(false);
      setAskquery({ ...Askquery, query: "" })
    }
  }

  const getallData = () => {
    dispatch(getallIds());
  }

  useEffect(() => {
    getallData();
  }, [])

  useEffect(() => {
    setAskquery({ ...Askquery, id: id })
  }, [id])

  const handleQuery = (e) => {
    setAskquery({ ...Askquery, [e.target.name]: e.target.value })
  }
  const isHidden = Askquery?.id ? { display: 'none' } : {};
  const handlechange = (e) => {
    setvideolink({ ...videolink, [e.target.name]: e.target.value })
  }
  const OpenModel = () => {
    setopen(true);
  }
  const closeModel = () => {
    if (!load) {
      setopen(false);
    }
  }

  const sethandleId = async (id) => {
    await dispatch(SaveId(id));
  }
  console.log(videolink);

  const handleprocess = async () => {
    setload(true);
    try {
      const res = await Process_video(videolink);
      let id = res?.data?.data?.id;
      console.log(id);
      const checkStatus = async () => {
        const ress = await CheckProcess(id);
        if (ress.status === 200) {
          await dispatch(SaveId(id));
          toast.success("Processed Successfully! Ask Question Now");
          setload(false);
          setopen(false);
          getallData();
          clearInterval(intervalId);
        }
        else {
          // toast.error("please wait !!");
        }
      };

      const intervalId = setInterval(checkStatus, 5000);

    } catch (error) {
      console.error('Error processing video:', error);
      setload(false);
    }
  };

  console.log(chat);
  console.log(container);

  return (
    <>
      <div className='home'>
        {/* Toggle bar */}
        <div className='toggle'>
          <FaToggleOff className='toggle_btn' color='white' fontSize='40px' />
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
            <div className='txt'>
              <img src={logo} className='logo_home'></img>
              <h2 style={{ fontWeight: "400" }} onClick={OpenModel}>Upload the video</h2>
            </div>
          </div>
          <h4 style={{ fontSize: "20px", color: "white", fontWeight: "400", marginLeft: "20px" }}>Chat with earlier video</h4>
          <hr style={{ marginBottom: "30px", width: "90%", height: "2px", border: "none", backgroundColor: "gray" }}></hr>
          <div style={{ width: "100%", height: "70vh", display: "flex", alignItems: "center", flexDirection: "column" }}>
            {
              Ids?.map((ele) => {
                return (
                  <button className='earlier_video' onClick={() => sethandleId(ele.id)}>
                    <h3>{ele.extracted_text.split(' ').slice(0, 4).join(' ')} . . .</h3>
                  </button>
                )
              })
            }
          </div>
        </div>
        <div className='container'>
          <div className='answer_box'>
            {
              id ?
                <h1 className='IdName'>Current ID - {id}</h1>
                :
                <></>
            }
            <button style={{ position: "absolute", top: "20px", right: "20px", height: "40px", width: "40px", fontSize: "25px", borderRadius: "100%", cursor: "pointer" }}>N</button>
            {
              !container ?
                <div style={{ height: "318px", width: "901px", display: "flex", justifyContent: "center", flexDirection: "column", alignItems: "center", ...isHidden }}>
                  <img src={logo} className='logo_home_c'></img>
                  <h1 className='chatheading'> ChatTube (Ask Query To Youtube Video)</h1>
                  <div style={{ display: "flex", justifyContent: "space-around", width: "100%" }}>
                    <div className='b1'>
                      <HiMiniPencilSquare fontSize='25px' color='white' className='a1' />
                      <h3 className='q1'>Get The Video Summary</h3>
                    </div>
                    <div className='b1'>
                      <FaRegLightbulb fontSize='25px' color='white' className='a1' />
                      <h3 className='q1'>Increasing Productivity</h3>
                    </div>
                    <div className='b1'>
                      <IoCodeSlash fontSize='25px' color='white' className='a1' />
                      <h3 className='q1'>Learning in Less Time</h3>
                    </div>
                    <div className='b1'>
                      <LiaHandsHelpingSolid fontSize='25px' color='white' className='a1' />
                      <h3 className='q1'>Helpful For Deaf People</h3>
                    </div>
                  </div>
                </div>
                :
                <div className='chat'>
                  {
                    chat?.map((ele) => {
                      return (
                        <div>
                          <div className='user_message_div'>
                            <img src={user} className='user_img' alt="User" />
                            <h3 className='User'>{ele.user_content}</h3>
                          </div>
                          <div className='ai_message_div'>
                            <img src={ai} className='ai_img' alt="AI" />
                            <h4 className='Ai'>{ele.ai_answer}</h4>
                          </div>
                        </div>
                      )
                    })
                  }
                  <div style={{display:"flex",justifyContent:"center",color:"white"}}>
                  {
                    loader?
                    <div class="loader"></div>
                    :
                    <></>
                  }
                  </div>
                </div>
            }
          </div>
          {
            container?
          <div className='query'>
            <div style={{ display: "flex", width: "100%", justifyContent: "center" }}>
              <input className='query_input' placeholder='Write the Query Related to the video ...' name='query' value={Askquery?.query} onChange={handleQuery} />
              <IoIosSend color='white' fontSize='60px' className='send' onClick={send} />
            </div>
            <h2 style={{ fontSize: "14px", color: "white" }}>ChatTube can make mistake . Check important info .</h2>
          </div>
          :
          <></>
            }
        </div>
      </div>
      {
        open ?
          <div className='OpenUploadModal'>
            <div className='modelConatiner'>
              <IoMdClose fontSize="30px" style={{ position: "absolute", top: "10px", right: "13px", cursor: "pointer" }} onClick={closeModel} />
              <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "47px", marginBottom: "30px" }}>
                <img src={logo} style={{ height: "60px" }}></img>
                <h3 style={{ fontSize: "30px" }}>ChatTube</h3>
              </div>
              {
                load ?
                  <div class="loader1"></div>
                  :
                  <></>
              }
              <input style={{ height: "50px", width: "80%", fontSize: "20px" }} placeholder='Enter The Video Link Here . . .' name='Youtube_link' value={videolink?.Youtube_link} onChange={handlechange}></input>
              {
                load ?
                  <button style={{ height: "50px", width: "250px", fontSize: "20px", borderRadius: "10px", border: "1px solid black", cursor: "pointer" }} >PreProcess The Video</button>
                  :
                  <button style={{ height: "50px", width: "250px", fontSize: "20px", borderRadius: "10px", border: "1px solid black", cursor: "pointer" }} onClick={handleprocess}>PreProcess The Video</button>
              }
            </div>
          </div>
          :
          <></>
      }
    </>
  )
}
