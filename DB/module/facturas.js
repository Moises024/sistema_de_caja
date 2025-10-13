import dataBase from "./db.js";
import mongoose from "mongoose";
import AutoIncrementFactory from 'mongoose-sequence';

let Facturas;

const getFacturaModel = async () => {
  if (Facturas) return Facturas;

  const conn = await dataBase();
  const AutoIncrement = AutoIncrementFactory(mongoose);

  const facturaSchema = new mongoose.Schema({
    no_factura: Number,
    usuario_id: {
      type: mongoose.SchemaTypes.ObjectId,
      ref: "usuarios", // 💡 debe coincidir con el nombre del modelo de usuarios
      required: true
    },
    factura: { type: String, required: true },
    total: { type: Number, required: true },
    fecha: { type: Number,required:true },
    recibido: { type: Number,required:true,default:0 },
    devuelta: { type: Number,required:true, default:0},
  });

  facturaSchema.plugin(AutoIncrement, { inc_field: 'no_factura' });

  Facturas = conn.model("facturas", facturaSchema);
  return Facturas;
};

export default getFacturaModel;
