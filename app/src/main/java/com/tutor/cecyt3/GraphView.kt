package com.tutor.cecyt3

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.util.AttributeSet
import android.view.View

/**
 * Panel de dibujo simple: recibe una lista de puntos (x, y) en coordenadas
 * matemáticas y las convierte a coordenadas de pantalla, dibujando ejes
 * y la curva. No depende de ninguna librería externa (100% offline).
 */
class GraphView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : View(context, attrs) {

    private var puntos: List<Pair<Double, Double>> = emptyList()

    private val paintEjes = Paint().apply {
        color = Color.DKGRAY
        strokeWidth = 3f
    }
    private val paintCurva = Paint().apply {
        color = Color.parseColor("#1976D2")
        strokeWidth = 6f
        style = Paint.Style.STROKE
        isAntiAlias = true
    }
    private val paintTexto = Paint().apply {
        color = Color.GRAY
        textSize = 24f
    }

    fun setPuntos(nuevosPuntos: List<Pair<Double, Double>>) {
        puntos = nuevosPuntos
        invalidate()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (puntos.isEmpty()) return

        val xs = puntos.map { it.first }
        val ys = puntos.map { it.second }
        val xMin = xs.min()
        val xMax = xs.max()
        val yMin = ys.min()
        val yMax = ys.max()

        val margen = 60f
        val anchoUtil = width - 2 * margen
        val altoUtil = height - 2 * margen

        // Evita división entre cero si la función es constante
        val rangoX = if (xMax - xMin == 0.0) 1.0 else xMax - xMin
        val rangoY = if (yMax - yMin == 0.0) 1.0 else yMax - yMin

        fun mapX(x: Double): Float = (margen + ((x - xMin) / rangoX) * anchoUtil).toFloat()
        fun mapY(y: Double): Float = (height - margen - ((y - yMin) / rangoY) * altoUtil).toFloat()

        // Eje X (y = 0) y eje Y (x = 0), si entran en el rango visible
        if (yMin <= 0 && yMax >= 0) {
            val yEje = mapY(0.0)
            canvas.drawLine(margen, yEje, width - margen, yEje, paintEjes)
        }
        if (xMin <= 0 && xMax >= 0) {
            val xEje = mapX(0.0)
            canvas.drawLine(xEje, margen, xEje, height - margen, paintEjes)
        }

        // Curva: se conecta punto a punto, pero se corta si hay un salto brusco
        // (indica una asíntota / discontinuidad)
        var prev: Pair<Double, Double>? = null
        for (p in puntos) {
            if (prev != null) {
                canvas.drawLine(
                    mapX(prev.first), mapY(prev.second),
                    mapX(p.first), mapY(p.second),
                    paintCurva
                )
            }
            prev = p
        }

        canvas.drawText("x: [%.2f, %.2f]".format(xMin, xMax), margen, 30f, paintTexto)
        canvas.drawText("y: [%.2f, %.2f]".format(yMin, yMax), margen, height - 15f, paintTexto)
    }
}
