package com.tutor.cecyt3

import android.content.Intent
import android.os.Bundle
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity
import com.tutor.cecyt3.databinding.ActivityMateriaBinding

class MateriaActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMateriaBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMateriaBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val materia = intent.getStringExtra("materia") ?: return
        title = Materias.nombresBonitos[materia] ?: materia

        val ramas = Materias.ramasPorMateria[materia] ?: emptyList()
        ramas.forEach { rama ->
            val boton = Button(this).apply {
                text = Materias.nombresRamas[rama] ?: rama
                layoutParams = LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
                ).apply { topMargin = 16 }
                setOnClickListener {
                    val intent = Intent(this@MateriaActivity, FormularioActivity::class.java)
                    intent.putExtra("materia", materia)
                    intent.putExtra("rama", rama)
                    startActivity(intent)
                }
            }
            binding.contenedorRamas.addView(boton)
        }
    }
}
