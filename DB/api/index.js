import { cors } from "../funciones/cors.js"
import Usuario from "../module/usuarios.js"
export default function handler(req, res) {
    cors(req, res)
    console.log(Usuario)
   
    const crearUsuario =  async () => {
        
        const usuario_data = {
            nombre: "Moises",
            apellido: "Zabala",
            contra: "123",
            usuario: "Moises024"

        }
        const usuario = await new Usuario(usuario_data)
        await usuario.save()
        res.json({ ok: usuario })
    }
    crearUsuario()
}