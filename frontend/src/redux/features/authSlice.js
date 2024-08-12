import { createSlice } from '@reduxjs/toolkit';
import * as api from '../api';
import { toast } from 'react-toastify';

// Initialize state with token from local storage if available
const initialState = {
  isAuthenticated: !!localStorage.getItem('token'),
  token: localStorage.getItem('token') || null,
  error: null,
  user: null,
  loading: false,
  id:null,
  Ids : [],
  chat: []
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    loginStart(state) {
      state.loading = true;
      state.error = null;
    },
    loginSuccess(state, action) {
      state.isAuthenticated = true;
      state.token = action.payload.access_token;
      state.user = action.payload.data;
      state.error = null;
      state.loading = false;
      localStorage.setItem('token', action.payload.access_token); // Save token to local storage
    },
    loginFail(state, action) {
      state.loading = false;
      state.token = null;
      state.isAuthenticated = false;
      state.error = action.payload;
      localStorage.removeItem('token'); // Remove token from local storage on failure
    },
    Logout(state) {
      state.isAuthenticated = false;
      state.token = null;
      state.error = null;
      state.loading = false;
      localStorage.removeItem('token'); // Remove token from local storage on logout
    },
    SaveId(state,action){
      state.id = action.payload;
    },
    SaveIdsArray(state,action){
      state.Ids = action.payload.data;
    },
    SaveChatHistory(state,action){
      state.chat = action.payload.data.chathistory
    }
  },
});

export const {
  loginStart,
  loginSuccess,
  loginFail,
  Logout,
  SaveId,
  SaveIdsArray,
  SaveChatHistory
} = authSlice.actions;

export const { reducer: authReducer } = authSlice;

const loginDispatcher = (login) => async (dispatch) => {
  try {
    dispatch(loginStart());
    const response = await api.login(login);
    console.log(response);
    if (response.status === 200) {
      dispatch(loginSuccess(response.data.data));
      toast.success("Login successful");
      return response;
    }
  } catch (error) {
    console.log(error);
    toast.error("Something went wrong");
    dispatch(loginFail("Something went wrong"));
  }
}

const registerDispatcher = (register) => async (dispatch) => {
  try {
    const response = await api.register(register);
    console.log(response);
    if (response.status === 200) {
      toast.success("Registered successfully");
      return response;
    }
  } catch (error) {
    console.log(error);
    toast.error("Something went wrong");
    dispatch(loginFail("Something went wrong"));
  }
}
const Process_video = async (videolink) => {
  try {
    const res = await api.process(videolink);
    console.log(res);
    return res;
  } catch (error) {
    console.error('Error processing video:', error);
  }
};

const CheckProcess = async (id) =>{
  try {
    const res = await api.check(id);
    console.log(res);
    return res;
  } catch (error) {
    return error;
    // console.error('Currently processing:', error);
  }
}

const getallIds = () => async (dispatch) =>{
  try {
    const res = await api.getall();
    console.log(res);
    if (res.status === 200) {
      dispatch(SaveIdsArray(res));
      return res;
    }
    } catch (error) {
    console.log(error);
    return error;
  }
}

const SendQuery = (Askquery) => async (dispatch) => {
  try {
    const res = await api.Answer(Askquery);
    console.log(res);
    return res;
  } catch (error) {
    console.log(error);
  }
}

const getHistory = (id) => async (dispatch) => {
  try {
    const res = await api.GetHistoryById(id) 
    console.log(res);
    if(res.status == 200){
      dispatch(SaveChatHistory(res.data))
    }
  } catch (error) {
    console.log(error);
  }
}

export { loginDispatcher, registerDispatcher , Process_video ,CheckProcess ,getallIds , SendQuery , getHistory};
export default authSlice.reducer;