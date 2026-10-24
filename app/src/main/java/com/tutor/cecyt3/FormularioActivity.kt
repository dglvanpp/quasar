package com.tutor.cecyt3

import android.graphics.Color
import android.os.Bundle
import android.view.HapticFeedbackConstants
import android.view.View
import android.view.ViewGroup
import android.webkit.WebView
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.tutor.cecyt3.databinding.ActivityFormularioBinding
import org.json.JSONException
import org.json.JSONObject

class FormularioActivity : AppCompatActivity() {

    private lateinit var binding: ActivityFormularioBinding
    private lateinit var materia: String
    private lateinit var rama: String
    private var campos: List<CampoFormulario> = emptyList()

    private val vistasEntrada = mutableMapOf<String, View>()
    private val filas = mutableMapOf<String, LinearLayout>()
    private var focusedEditText: EditText? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityFormularioBinding.inflate(layoutInflater)
        setContentView(binding.root)

        materia = intent.getStringExtra("materia") ?: return
        rama = intent.getStringExtra("rama") ?: return
        title = Materias.nombresRamas[rama] ?: rama

        // Validación de seguridad por si la rama no existe en las definiciones
        campos = FormDefinitions.definiciones[rama] ?: emptyList()

        val prellenadoJson = intent.getStringExtra("datos_prellenados")
        val prellenado = if (prellenadoJson != null) JSONObject(prellenadoJson) else null

        construirCampos(prellenado)

        // Habilitamos el WebView para que el diseño neón se pueda dibujar
        binding.visorMatematico.settings.javaScriptEnabled = true
        binding.visorMatematico.setBackgroundColor(Color.parseColor("#000000"))

        binding.btnResolver.setOnClickListener { view ->
            view.performHapticFeedback(HapticFeedbackConstants.CONFIRM)
            resolver()
        }

        configurarTeclado()
    }

    private fun configurarTeclado() {
        val teclado = binding.tecladoMatematico
        val botones = mapOf(
            teclado.btnX to "x",
            teclado.btnPotencia to "^",
            teclado.btnRaiz to "sqrt()",
            teclado.btnSin to "sin()",
            teclado.btnCos to "cos()",
            teclado.btnTan to "tan()",
            teclado.btnSec to "sec()",
            teclado.btnCsc to "csc()",
            teclado.btnCot to "cot()",
            teclado.btnPi to "pi"
        )

        botones.forEach { (boton, texto) ->
            boton.setOnClickListener {
                focusedEditText?.let { et ->
                    val start = et.selectionStart
                    val end = et.selectionEnd
                    et.text.replace(start, end, texto)
                    
                    // Si el texto termina en (), ponemos el cursor adentro
                    if (texto.endsWith("()")) {
                        et.setSelection(start + texto.length - 1)
                    } else {
                        et.setSelection(start + texto.length)
                    }
                    et.requestFocus()
                }
            }
        }
    }

    private fun construirCampos(prellenado: JSONObject?) {
        for (campo in campos) {
            val fila = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
                ).apply { topMargin = 20 }
            }

            val label = TextView(this).apply { text = campo.etiqueta }
            fila.addView(label)

            when (campo.tipo) {
                TipoCampo.SELECTOR -> {
                    val spinner = Spinner(this)
                    spinner.adapter = ArrayAdapter(
                        this, android.R.layout.simple_spinner_dropdown_item, campo.opciones ?: emptyList()
                    )
                    spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                        override fun onItemSelected(p: AdapterView<*>?, v: View?, pos: Int, id: Long) {
                            actualizarVisibilidad()
                        }
                        override fun onNothingSelected(p: AdapterView<*>?) {}
                    }
                    fila.addView(spinner)
                    vistasEntrada[campo.clave] = spinner
                }
                else -> {
                    val input = EditText(this).apply {
                        hint = when (campo.tipo) {
                            TipoCampo.LISTA_NUMEROS -> "ej. 12.5, 12.6, 12.4, 12.8"
                            TipoCampo.TEXTO -> "escribe aquí"
                            else -> "opcional"
                        }
                        inputType = if (campo.tipo == TipoCampo.NUMERO)
                            android.text.InputType.TYPE_CLASS_NUMBER or android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL or android.text.InputType.TYPE_NUMBER_FLAG_SIGNED
                        else
                            android.text.InputType.TYPE_CLASS_TEXT
                        prellenado?.optString(campo.clave, null)?.let { setText(it) }

                        setOnFocusChangeListener { _, hasFocus ->
                            if (hasFocus) focusedEditText = this
                        }
                    }
                    fila.addView(input)
                    vistasEntrada[campo.clave] = input
                }
            }

            filas[campo.clave] = fila
            binding.contenedorCampos.addView(fila)
        }
        actualizarVisibilidad()
    }

    private fun actualizarVisibilidad() {
        for (campo in campos) {
            val condicion = campo.mostrarSoloSi ?: continue
            val (claveSelector, valoresQueActivan) = condicion
            val spinner = vistasEntrada[claveSelector] as? Spinner
            val valorActual = spinner?.selectedItem as? String
            filas[campo.clave]?.visibility =
                if (valorActual != null && valoresQueActivan.contains(valorActual))
                    View.VISIBLE else View.GONE
        }
    }

    // EL TRADUCTOR AUTOMÁTICO (El filtro mágico)
    private fun traducirParaPython(entrada: String): String {
        var ecuacion = entrada
        // 1. Cambia el símbolo de potencia normal por el de Python
        ecuacion = ecuacion.replace("^", "**")
        // 2. Agrega el asterisco de multiplicación entre números y letras (Ej: 4x -> 4*x)
        val regex = Regex("(\\d)([a-zA-Z])")
        ecuacion = ecuacion.replace(regex, "$1*$2")
        return ecuacion
    }

    private fun resolver() {
        val py = Python.getInstance()
        val builtins = py.getModule("builtins")
        val datosPy: PyObject = builtins.callAttr("dict")

        for (campo in campos) {
            if (filas[campo.clave]?.visibility != View.VISIBLE) continue

            when (campo.tipo) {
                TipoCampo.SELECTOR -> {
                    val spinner = vistasEntrada[campo.clave] as Spinner
                    val valor = spinner.selectedItem as? String
                    if (!valor.isNullOrEmpty()) datosPy.callAttr("__setitem__", campo.clave, valor)
                }
                TipoCampo.LISTA_NUMEROS -> {
                    val input = vistasEntrada[campo.clave] as EditText
                    val texto = input.text.toString().trim()
                    if (texto.isNotEmpty()) {
                        val lista = texto.split(",")
                            .mapNotNull { it.trim().toDoubleOrNull() }
                        datosPy.callAttr("__setitem__", campo.clave, lista)
                    }
                }
                else -> {
                    val input = vistasEntrada[campo.clave] as EditText
                    var texto = input.text.toString().trim()

                    // APLICAMOS EL FILTRO TRADUCTOR A LOS CAMPOS DE TEXTO LIBRE
                    if (texto.isNotEmpty()) {
                        texto = traducirParaPython(texto)
                        datosPy.callAttr("__setitem__", campo.clave, texto)
                    }
                }
            }
        }

        // ==============================================================
        // AQUÍ ESTÁ EL SALVAVIDAS (TRY-CATCH) PARA EVITAR EL CRASHEO
        // ==============================================================
        try {
            // NOTA: Asegúrate de que tu archivo de Python se llame exactamente "tutor_cecyt.py"
            val router = py.getModule("tutor_cecyt")
            val resultado = router.callAttr("procesar_consulta_android", materia, rama, datosPy)

            // Limpiamos los views anteriores de Android
            binding.contenedorResultado.removeAllViews()

            // Inyectamos el resultado al único lienzo KaTeX
            renderizarConMathJax(binding.visorMatematico, resultado.toString())

        } catch (e: Exception) {
            // Si Python falla, atrapamos el error y lo mostramos en la pantalla en lugar de cerrar la app
            binding.contenedorResultado.removeAllViews()
            renderizarConMathJax(binding.visorMatematico, "Error interno del motor matemático:<br>${e.message}")
        }
    }

    /**
     * EL LIENZO ÚNICO: Reconstruido para armar el documento HTML con tarjetas neón
     * y renderizar TODOS los pasos y el resultado a través de KaTeX manualmente.
     */
    private fun renderizarConMathJax(webView: WebView, textoJson: String) {
        val json = try { JSONObject(textoJson) } catch (e: JSONException) { null }
        var htmlContent = ""

        if (json == null || !json.has("pasos")) {
            htmlContent = "<div style='color:#FF007F;'>$textoJson</div>"
        } else {
            // ARMANDO LAS TARJETAS DINÁMICAS EN HTML
            val pasos = json.optJSONArray("pasos")
            if (pasos != null) {
                for (i in 0 until pasos.length()) {
                    val paso = pasos.getJSONObject(i)
                    val titulo = paso.optString("titulo", "")
                    val contenido = paso.optString("contenido", "")

                    htmlContent += """
                        <div class="paso-tarjeta">
                            <div class="paso-titulo">$titulo</div>
                            <div class="math-content">$contenido</div>
                        </div>
                    """.trimIndent()
                }
            }

            val exito = json.optBoolean("exito", false)
            val resultadoFinal = json.optString("resultado_final", "")
            if (resultadoFinal.isNotEmpty()) {
                htmlContent += """
                    <div class="resultado-final">
                        <div style="color: #FF007F; font-size: 14px; margin-bottom: 10px;">Resultado Final</div>
                        <div class="math-content">$resultadoFinal</div>
                    </div>
                """.trimIndent()
            }
        }

        val htmlPlantilla = """
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" href="file:///android_asset/katex/katex.min.css">
                <script src="file:///android_asset/katex/katex.min.js"></script>
                <style>
                    body {
                        background-color: #000000;
                        color: #FFFFFF;
                        font-family: sans-serif;
                        margin: 0;
                        padding: 16px;
                    }
                    .paso-tarjeta {
                        background-color: #121212;
                        border-radius: 16px;
                        padding: 16px;
                        margin-bottom: 12px;
                        border-left: 4px solid #00E5FF; /* Neón Cian */
                    }
                    .paso-titulo {
                        color: #00E5FF;
                        font-weight: bold;
                        margin-bottom: 8px;
                        font-size: 14px;
                    }
                    .resultado-final {
                        background-color: #1a0010;
                        border-radius: 16px;
                        padding: 20px;
                        margin-top: 24px;
                        border: 2px solid #FF007F; /* Neón Magenta */
                        text-align: center;
                        font-size: 20px;
                    }
                    .math-content {
                        text-align: center;
                        font-size: 18px;
                        margin-top: 8px;
                        overflow-x: auto;
                    }
                </style>
            </head>
            <body>
                $htmlContent
                
                <script>
                    var elementos = document.getElementsByClassName("math-content");
                    for (var i = 0; i < elementos.length; i++) {
                        var ecuacion = elementos[i].innerText;
                        katex.render(ecuacion, elementos[i], {
                            throwOnError: false,
                            displayMode: true
                        });
                    }
                </script>
            </body>
            </html>
        """.trimIndent()

        webView.loadDataWithBaseURL("file:///android_asset/", htmlPlantilla, "text/html", "UTF-8", null)
    }
}