
import getUsuarioModel from "../module/usuarios.js"
export const register = async (req, res) => {
    try {
        const Usuario = await getUsuarioModel()
        const data = req.body
        const data_user = {
            nombre: data[0],
            contra: data[1],
            apellido: data[2],
            usuario: data[3]

        }
        const usuario = await new Usuario(data_user)
        await usuario.save()
        res.json({ ok: true, res: "Usuario creado correctamente." })
    } catch (err) {
        console.log(err)
        res.json({ ok: false, res: "No se pudo crear el usuario." })
    }
}
export const getUser = async (req, res) => {
    try {
        const Usuario = await getUsuarioModel()
        const data = await Usuario.find({})

        res.json({ ok: true, res: data })
    } catch (err) {
        res.json({ ok: false, res: "No se pudieron buscar los datos." })
    }
}