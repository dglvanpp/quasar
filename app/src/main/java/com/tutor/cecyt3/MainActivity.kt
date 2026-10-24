package com.tutor.cecyt3

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import com.tutor.cecyt3.databinding.ActivityMainBinding
import org.json.JSONObject

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        binding.cardMatematicas.setOnClickListener { abrirMateria("matematicas") }
        binding.cardFisica.setOnClickListener { abrirMateria("fisica") }
        binding.cardQuimica.setOnClickListener { abrirMateria("quimica") }
        binding.cardProbabilidad.setOnClickListener { abrirMateria("probabilidad") }
        binding.cardGraficas.setOnClickListener {
            startActivity(Intent(this, GraficadoraActivity::class.java))
        }
    }

    private fun abrirMateria(materia: String) {
        val intent = Intent(this, MateriaActivity::class.java)
        intent.putExtra("materia", materia)
        startActivity(intent)
    }
}
