import { deleteCliente, getCliente,setCliente,updateCliente } from "../funciones/cliente.js"
import { cors } from "../funciones/cors.js"



export default function handler(req,res){
    cors(req,res)
    
    if(req.method === "POST"){

        if(parseInt(req.headers["id"]) === 0)
        {
            
            
            return setCliente(req,res)
        }
        
        if(parseInt(req.headers["id"]) === 1)
        {
            return updateCliente(req,res)
        }

    }
    if(parseInt(req.headers["id"]) === 3){
        return deleteCliente(req,res)
    }
    return getCliente(req,res)

}