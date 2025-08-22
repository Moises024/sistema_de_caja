
import { cors } from "../funciones/cors";
export default function handler(req,res){
        cors(req,res)
        if(req.method === "POST"){
            
            return
        }
        res.json({ok:false,res:"ruta no valida"})
}
