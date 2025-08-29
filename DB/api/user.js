
import { cors } from "../funciones/cors.js";
import { getUser,register } from "../funciones/user.js";

export default function handler(req,res){
        cors(req,res)
        if(req.method === "POST"){

            return register(req,res)
        }
        return getUser(req,res)
}
