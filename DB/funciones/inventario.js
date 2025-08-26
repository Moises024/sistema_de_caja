import getFacturaModel from "../module/facturas.js"
import getUsuarioModel from "../module/usuarios.js"
export const addInventario = async (req, res) => {


    try {
        const Facturas = await getFacturaModel()
        const data = req.body
        const data_factura = {
            usuario_id: data[0],
            factura: data[1],
            total: data[2]
        }
        const factura = await new Facturas(data_factura)
        
        await factura.save()
        res.json({ ok: true, res: "Factura agregada correctamente." })
    } catch (error) {
        res.json({ ok: true, res: "No se pudo agregar dicha factura.", error })
    }
}
export const getInventario = async (req, res) => {

    try {
        await getUsuarioModel(); 
        const Facturas = await getFacturaModel()
        const data = await Facturas.find({})
        .sort({_id:-1})
        .populate({
            path: "usuario_id",
            select: "nombre usuario rol apellido id "

        })
        res.json({ ok: true, res: data })
    } catch (error) {
        console.log(error)
        res.json({ ok: true, res: "No se pudo encontrar dicha factura.", error })
    }
}
export const delInventario = async (req, res) => {


    try {
        const Facturas = await getFacturaModel()
        const data = req.body
        await Facturas.findOneAndDelete({ id: data._id })

        res.json({ ok: true, res: "Factura eliminado correctamente" })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo eliminar el factura.", error: err })
    }
}