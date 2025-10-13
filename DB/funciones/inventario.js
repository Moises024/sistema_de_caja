import getFacturaModel from "../module/facturas.js"
import getUsuarioModel from "../module/usuarios.js"
import mongoose from 'mongoose';
export const addInventario = async (req, res) => {


    try {
        const data = req.body
        const Facturas = await getFacturaModel()

        const data_factura = {
            usuario_id: data[0],
            factura: data[1],
            total: data[2],
            fecha: data[3],
            recibido: data[6],
            devuelta: data[7]
        }
        const factura = await new Facturas(data_factura)
        console.log(factura)
        await factura.save()
        req.headers["_id"] = factura._id
        await getInventarioNumber(req, res)
        // res.json({ ok: true, res: "Factura agregada correctamente." })
    } catch (error) {

        res.json({ ok: true, res: "No se pudo agregar dicha factura.", error })
    }
}
export const getInventario = async (req, res) => {

    try {
        await getUsuarioModel();
        const Facturas = await getFacturaModel()
        const data = await Facturas.find({})
            .sort({ _id: -1 })
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
        const eliminado = await Facturas.findOneAndDelete({ no_factura: data._id })
        if (!eliminado) {
            res.json({ ok: false, res: "No se pudo eliminar el factura.", error: err })
            return
        }
        res.json({ ok: true, res: "Factura eliminado correctamente" })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo eliminar el factura.", error: err })
    }
}
export const getInventarioUsuario = async (req, res) => {
    try {
        const data = req.body
        const Facturas = await getFacturaModel()
        const datos = await Facturas.find({
            fecha: {
                $gte: data[0],
                $lte: data[1]
            }, usuario_id: data[2]
        })

        res.json({ ok: true, res: datos })
    } catch (error) {
        console.log(error)

        res.json({ ok: false, res: "No se pudo encontrar dicha factura.", error })
    }
}
export const getInventarioNumber = async (req, res) => {
    try {


        const id = req.headers["_id"]
        const Facturas = await getFacturaModel()
        let datos
        if (!id) {
            datos = await getCurrentFacturaSeq()
            res.json({ ok: true, res: datos })
            return
        }

        datos = await Facturas.findOne({ _id: id })
        res.json({ ok: true, res: datos.no_factura })

    } catch (error) {
        console.log(error)
        res.json({ ok: false, res: "No se pudo encontrar dicha factura.", error })
    }
}



export const getCurrentFacturaSeq = async () => {
    const conn = mongoose.connection;

    const counter = await conn
        .collection('counters')
        .find()
        .pretty()
    console.log(counter)
    return counter?.seq ?? 0; // si no existe, devuelve 0
};