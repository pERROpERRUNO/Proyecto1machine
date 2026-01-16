from manim import *
import numpy as np

class RegressionDemo(Scene):
    def construct(self):
        self.introduccion()
        self.regresion_lineal_optimizada()
        self.regresion_no_lineal_optimizada()
        self.underfitting_overfitting()
        self.comparativa_final()
        self.conclusiones()

    #  INTRODUCCIÓN 
    def introduccion(self):
        titulo = Text("Análisis de Regresión", font_size=48, color=BLUE)
        subtitulo = Text("Modelos Lineales y No Lineales", font_size=32).next_to(titulo, DOWN)

        nombres = VGroup(
            Text("Grupo 6", font_size=24, color=GRAY),
            Text("Ricardo Meza • Miguel Ramos • Mateo Silva", font_size=20, color=GRAY)
        ).arrange(DOWN).to_edge(DOWN)

        self.play(Write(titulo))
        self.play(FadeIn(subtitulo, shift=UP))
        self.play(FadeIn(nombres))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(subtitulo), FadeOut(nombres))

    # GENERACIÓN DE DATA 
    def generar_data_lineal(self):
        x = np.linspace(0, 10, 30)
        y = 1.2 * x + 2 + np.random.normal(0, 0.5 , len(x))
        y[5] += 3  # outlier
        return x, y

    def generar_data_no_lineal(self):
        x = np.linspace(0, 4, 40)
        y = 0.5 * x**3 - 2 * x**2 + 3*x + 1 + np.random.normal(0, 0.5, len(x))
        return x, y

    #  REGRESIÓN LINEAL 
    def regresion_lineal_optimizada(self):
        header = Title("1. Regresión Lineal")
        self.add(header)

        ejes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 20, 2],
            axis_config={"include_numbers": True}
        ).scale(0.7).shift(DOWN*0.5)

        x, y = self.generar_data_lineal()
        puntos = VGroup(*[Dot(ejes.c2p(xi, yi), color=BLUE) for xi, yi in zip(x, y)])

        # Trackers
        w = ValueTracker(0.3)
        b = ValueTracker(5)

        # Línea y residuos dinámicos
        linea = always_redraw(lambda: ejes.plot(lambda t: w.get_value()*t + b.get_value(), color=YELLOW))
        residuos = always_redraw(lambda: VGroup(*[
            Line(ejes.c2p(xi, yi), ejes.c2p(xi, w.get_value()*xi + b.get_value()), color=RED, stroke_width=2)
            for xi, yi in zip(x, y)
        ]))

        # Parámetros visibles
        w_text = always_redraw(lambda: MathTex(f"w={w.get_value():.2f}", color=YELLOW).to_corner(UL).shift(DOWN))
        b_text = always_redraw(lambda: MathTex(f"b={b.get_value():.2f}", color=YELLOW).next_to(w_text, DOWN))
        formula = MathTex("y = wx + b", color=YELLOW).next_to(b_text, DOWN)

        self.play(Create(ejes), FadeIn(puntos))
        self.play(Create(linea), Create(residuos), FadeIn(w_text), FadeIn(b_text), Write(formula))
        self.wait(1)
        self.play(w.animate.set_value(1.15), b.animate.set_value(2.2), run_time=4)
        self.wait(2)
        self.play(FadeOut(VGroup(ejes, puntos, linea, residuos, w_text, b_text, formula, header)))

    #  REGRESIÓN NO LINEAL 
    def regresion_no_lineal_optimizada(self):
        header = Title("2. Regresión No Lineal")
        self.add(header)

        ejes = Axes(
            x_range=[0, 4, 0.5],
            y_range=[0, 25, 5],
            axis_config={"include_numbers": True}
        ).scale(0.7).shift(DOWN*0.5)

        x, y = self.generar_data_no_lineal()
        puntos = VGroup(*[Dot(ejes.c2p(xi, yi), color=PURPLE) for xi, yi in zip(x, y)])

        # Trackers
        a = ValueTracker(0.1)
        b = ValueTracker(-0.5)
        c = ValueTracker(1.0)
        d = ValueTracker(2.0)

        curva = always_redraw(lambda: ejes.plot(
            lambda t: a.get_value()*t**3 + b.get_value()*t**2 + c.get_value()*t + d.get_value(),
            x_range=[0,4], color=PINK
        ))

        residuos = always_redraw(lambda: VGroup(*[
            Line(
                ejes.c2p(xi, yi),
                ejes.c2p(xi, a.get_value()*xi**3 + b.get_value()*xi**2 + c.get_value()*xi + d.get_value()),
                color=ORANGE, stroke_width=2
            )
            for xi, yi in zip(x, y)
        ]))

        coef_text = always_redraw(lambda: MathTex(
            f"a={a.get_value():.2f}, b={b.get_value():.2f}, c={c.get_value():.2f}, d={d.get_value():.2f}",
            font_size=30, color=PINK
        ).to_corner(UL).shift(DOWN))
        formula = MathTex("y = ax^3 + bx^2 + cx + d", color=PINK).next_to(coef_text, DOWN)

        self.play(Create(ejes), FadeIn(puntos))
        self.play(Create(curva), Create(residuos), FadeIn(coef_text), Write(formula))
        self.wait(1)
        self.play(a.animate.set_value(0.5), b.animate.set_value(-2.0),
                  c.animate.set_value(3.0), d.animate.set_value(1.0), run_time=5)
        self.wait(2)
        self.play(FadeOut(VGroup(ejes, puntos, curva, residuos, coef_text, formula, header)))

    #  UNDERFITTING Y OVERFITTING 
    def underfitting_overfitting(self):
        header = Title("3. Underfitting vs Overfitting")
        self.add(header)

        ejes = Axes(x_range=[0,4,0.5], y_range=[0,25,5],
                    axis_config={"include_numbers": True}).scale(0.7).shift(DOWN*0.5)

        x, y = self.generar_data_no_lineal()
        puntos = VGroup(*[Dot(ejes.c2p(xi, yi), color=WHITE, radius=0.05) for xi, yi in zip(x, y)])

        # Underfitting: recta simple
        w = ValueTracker(1.0)
        b = ValueTracker(2.0)
        linea_under = always_redraw(lambda: ejes.plot(lambda t: w.get_value()*t + b.get_value(), x_range=[0,4], color=RED))
        label_under = Text("Underfitting\nModelo simple", font_size=22, color=RED).to_corner(UL).shift(DOWN)

        # Overfitting: polinomio + ondulación
        coef = ValueTracker(0.0)
        curva_over = always_redraw(lambda: ejes.plot(
            lambda t: 0.5*t**3 -2*t**2 + 3*t +1 + coef.get_value()*np.sin(6*t),
            x_range=[0,4], color=BLUE
        ))
        label_over = Text("Overfitting\nModelo complejo", font_size=22, color=BLUE).to_corner(UR).shift(DOWN)

        # Animación
        self.play(Create(ejes), FadeIn(puntos))
        self.wait(2)
        self.play(Create(linea_under), Write(label_under))
        self.wait(2)
        self.play(FadeOut(linea_under), FadeOut(label_under))
        self.play(Create(curva_over), Write(label_over))
        self.play(coef.animate.set_value(0.8), run_time=4)
        self.wait(2)
        self.play(FadeOut(VGroup(ejes, puntos, curva_over, label_over, header)))

    #  COMPARATIVA FINAL 
    def comparativa_final(self):
        header = Title("4. Comparativa y Elección del Modelo")
        self.add(header)

        texto = VGroup(
            Text("• Underfitting: el modelo no captura la forma de los datos.", font_size=28, color=RED),
            Text("• Overfitting: el modelo se ajusta demasiado al ruido.", font_size=28, color=BLUE),
            Text("• Modelo ideal: suficiente complejidad para capturar patrones sin sobreajustar.", font_size=28, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).shift(UP)

        self.play(Write(texto))
        self.wait(6)
        self.play(FadeOut(VGroup(texto, header)))

    #  CONCLUSIONES 
    def conclusiones(self):
        titulo = Text("Conclusiones", color=BLUE).to_edge(UP)
        puntos = VGroup(
            Text("1. La animación permite ver cómo se construye una regresión paso a paso.", font_size=26),
            Text("2. En regresión lineal se observa el ajuste de una recta a los datos.", font_size=26),
            Text("3. En regresión no lineal se muestra cómo cambia la curvatura del modelo.", font_size=26),
            Text("5. Los residuos animados permiten entender visualmente el error del ajuste.", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT).shift(UP*0.3)

        self.play(Write(titulo))
        for p in puntos:
            self.play(FadeIn(p, shift=LEFT))
            self.wait(1.2)
        self.wait(5)


