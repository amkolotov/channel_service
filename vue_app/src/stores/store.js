// import { defineStore } from 'pinia'
//
// export const useStore = defineStore({
//   id: 'index',
//   state: () => ({
//     backendUrl: "http://127.0.0.1:1337/api/v1"
//   }),
//   getters: {
//     getServerUrl: state => {
//             return state.backendUrl
//         }
//   }
// })
import { createStore } from 'vuex'

export default createStore({
  id: 'index',
  state: () => ({
    backendUrl: "http://127.0.0.1:8000/api/v1/"
  }),
  getters: {
    getServerUrl: state => {
            return state.backendUrl
        }
  }
})
