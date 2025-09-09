import dataBase from "./db.js";
import mongoose from "mongoose";
import AutoIncrementFactory from 'mongoose-sequence';

let Almacen;

const getAlmacenModel = async () => {
  if (Almacen) return Almacen;

  const conn = await dataBase();
  const AutoIncrement = AutoIncrementFactory(mongoose);

  const almacenSchema = new mongoose.Schema({
    id: Number,
    nombre: { type: String, required: true },
    cantidad: { type: Number, required: true },
    precio: { type: Number, required: true },
    costo: { type: Number, required: true },
    tipo: { type: String, default: null },

  });

  almacenSchema.plugin(AutoIncrement, { inc_field: 'id' });

  Almacen = conn.model("articulos", almacenSchema);
  return Almacen;
};

export default getAlmacenModel;
