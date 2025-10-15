
import getClienteModel from "../module/clientes.js"
import { actualizarEnvio } from "./inventario.js"
export const setCliente = async (req, res) => {
    const data = req.body
    const new_cliente = {
        nombre: data[0],
        telefono: data[1],
        sector: data[2]
    }
   
    try {
        const Cliente = await getClienteModel()
        const cliente = await new Cliente(new_cliente)
        await cliente.save()
        res.json({ ok: true, res: cliente._id })
    } catch (err) {
        res.json({ ok: false, res: err });
        
        
    }
}
export const getCliente = async (req, res) => {
    
    try{
        const Cliente = await getClienteModel()
        const cliente = await Cliente.find({})
        res.json({ ok: true, res: cliente })
    }catch(err)
    {
        res.json({ ok: true, res: err })   
    }
}

export const updateCliente = async (req, res) => {
    const data = req.body
    const envio = data[4]
    const Factura_id = data[5]
    const id = data[3]
    const cliente = {
        nombre: data[0],
        telefono: data[1],
        sector: data[2]
    }
    
    try {
        await actualizarEnvio([Factura_id,envio])
        const Cliente = await getClienteModel()
        const resp = await Cliente.updateOne({ _id: id }, {
            $set: cliente
        })

        res.json({ ok: true, res: "Loque sea" })
    } catch (err) {

        res.json({ ok: false, res: err })
    }


}
export const deleteCliente = async (req, res) => {
    try {

        const Cliente = await getClienteModel()
        await Cliente.deleteMany({})
        res.json({ ok: true, res: "all set" })
    } catch (eerr) {

    }



}