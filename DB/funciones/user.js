
import { database } from "../module/db.js"
export const register = async (req,res)=>{
    try{
        const data = req.body
        
        const cursor = await database()
        const user  = await cursor.connection.run("INSERT INTO usuarios(nombre,contra,apellido,usuario) VALUES(?, ?, ?, ?)",data)
        console.log(user)
        res.json({ok:true,res:"Usuario creado correctamente."})
    }catch(err){
        console.log(err)
        res.json({ok:false,res:"No se pudo crear el usuario."})
    }
}
export const getUser = async (req,res)=>{
    try{
        const cursor = await database()
        const data = await cursor.connection.all("SELECT * FROM usuarios")
        res.json({ok:true,res:data})
    }catch(err){
        res.json({ok:false,res:"No se pudieron buscar los datos."})
    }
}