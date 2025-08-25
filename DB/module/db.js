
import mongoose from "mongoose"
import { configDotenv } from "dotenv"
configDotenv()
 const dataBase =  async ()=>{
   try{
        const connect =  await mongoose.connect(process.env.URI,{})
        return  mongoose.connection

    }catch(err){
        console.log(err)
        console.log( "no conectado")
   }
   
}

export default dataBase