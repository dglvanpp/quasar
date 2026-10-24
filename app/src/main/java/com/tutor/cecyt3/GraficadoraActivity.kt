package com.tutor.cecyt3

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.tutor.cecyt3.databinding.ActivityGraficadoraBinding

class GraficadoraActivity : AppCompatActivity() {

    private lateinit var binding: ActivityGraficadoraBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityGraficadoraBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Valores por defecto para que el usuario no arranque en blanco
        binding.etFuncion.setText("x**2 - 3*x + 2")
        binding.etXMin.setText("-10")
        binding.etXMax.setText("10")

        binding.btnGraficar.setOnClickListener { graficar() }
    }

    private fun graficar() {
        val funcion = binding.etFuncion.text.toString().trim()
        val xMin = binding.etXMin.text.toString().toDoubleOrNull()
        val xMax = binding.etXMax.text.toString().toDoubleOrNull()

        if (funcion.isEmpty() || xMin == null || xMax == null || xMin >= xMax) {
            binding.tvErrorGrafica.text = "Revisa la función y que x mínimo sea menor que x máximo."
            return
        }
        binding.tvErrorGrafica.text = ""

        val py = Python.getInstance()
        val router = py.getModule("tutor_cecyt")
        val resultado: PyObject = router.callAttr("procesar_grafica", funcion, xMin, xMax)

        // La función Python devuelve una lista de [x, y] o un string de error
        if (resultado.type().toString().contains("str")) {
            binding.tvErrorGrafica.text = resultado.toString()
            return
        }

        val puntos = mutableListOf<Pair<Double, Double>>()
        for (item in resultado.asList()) {
            val par = item.asList()
            val x = par[0].toDouble()
            val y = par[1].toDouble()
            puntos.add(x to y)
        }

        binding.graphView.setPuntos(puntos)
    }
}
