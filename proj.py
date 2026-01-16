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

    # Regresión lineal 
    def regresion_lineal(self):
        title = Title("Regresión Lineal ")
        self.add(title)

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 20, 2],
            axis_config={"include_numbers": True}
        ).scale(0.7).shift(DOWN * 0.5)

        x, y = self.generar_data_lineal()
        points = VGroup(*[
            Dot(axes.c2p(xi, yi), color=BLUE) for xi, yi in zip(x, y)
        ])

        w = ValueTracker(0.0)
        b = ValueTracker(0.0)

        line = always_redraw(
            lambda: axes.plot(lambda t: w.get_value() * t + b.get_value(), color=YELLOW)
        )

        residuals = always_redraw(
            lambda: VGroup(*[
                Line(
                    axes.c2p(xi, yi),
                    axes.c2p(xi, w.get_value() * xi + b.get_value()),
                    color=RED,
                    stroke_width=2
                )
                for xi, yi in zip(x, y)
            ])
        )

        w_text = always_redraw(
            lambda: MathTex(f"w = {w.get_value():.2f}", color=YELLOW)
            .to_corner(UL).shift(DOWN)
        )

        b_text = always_redraw(
            lambda: MathTex(f"b = {b.get_value():.2f}", color=YELLOW)
            .next_to(w_text, DOWN)
        )

        formula = MathTex("y = wx + b", color=YELLOW).next_to(b_text, DOWN)

        self.play(Create(axes), FadeIn(points))
        self.play(Create(line), Create(residuals), FadeIn(w_text), FadeIn(b_text), Write(formula))
        self.wait(1)

        lr = 0.001
        epochs = 60

        for _ in range(epochs):
            y_pred = w.get_value() * x + b.get_value()
            error = y_pred - y

            dw = (2 / len(x)) * np.sum(error * x)
            db = (2 / len(x)) * np.sum(error)

            self.play(
                w.animate.set_value(w.get_value() - lr * dw),
                b.animate.set_value(b.get_value() - lr * db),
                run_time=0.1,
                rate_func=linear
            )

        self.wait(2)
        self.play(FadeOut(VGroup(axes, points, line, residuals, w_text, b_text, formula, title)))

    # Regresión no lineal con descenso por gradiente
    def regresion_no_lineal_gradiente(self):
        title = Title("Regresión No Lineal con Descenso por Gradiente")
        self.add(title)

        axes = Axes(
            x_range=[0, 4, 0.5],
            y_range=[0, 25, 5],
            axis_config={"include_numbers": True}
        ).scale(0.7).shift(DOWN * 0.5)

        x, y = self.generar_data_no_lineal()
        points = VGroup(*[
            Dot(axes.c2p(xi, yi), color=PURPLE) for xi, yi in zip(x, y)
        ])

        a = ValueTracker(0.0)
        b = ValueTracker(0.0)
        c = ValueTracker(0.0)
        d = ValueTracker(0.0)

        curve = always_redraw(
            lambda: axes.plot(
                lambda t: a.get_value()*t**3 + b.get_value()*t**2 +
                          c.get_value()*t + d.get_value(),
                x_range=[0, 4],
                color=PINK
            )
        )

        residuals = always_redraw(
            lambda: VGroup(*[
                Line(
                    axes.c2p(xi, yi),
                    axes.c2p(
                        xi,
                        a.get_value()*xi**3 + b.get_value()*xi**2 +
                        c.get_value()*xi + d.get_value()
                    ),
                    color=ORANGE,
                    stroke_width=2
                )
                for xi, yi in zip(x, y)
            ])
        )

        coef_text = always_redraw(
            lambda: MathTex(
                f"a={a.get_value():.2f}, b={b.get_value():.2f}, "
                f"c={c.get_value():.2f}, d={d.get_value():.2f}",
                font_size=30,
                color=PINK
            ).to_corner(UL).shift(DOWN)
        )

        formula = MathTex("y = ax^3 + bx^2 + cx + d", color=PINK).next_to(coef_text, DOWN)

        self.play(Create(axes), FadeIn(points))
        self.play(Create(curve), Create(residuals), FadeIn(coef_text), Write(formula))
        self.wait(1)

        lr = 0.0003
        epochs = 80

        for _ in range(epochs):
            y_pred = (
                a.get_value()*x**3 + b.get_value()*x**2 +
                c.get_value()*x + d.get_value()
            )

            error = y_pred - y

            da = (2 / len(x)) * np.sum(error * x**3)
            db = (2 / len(x)) * np.sum(error * x**2)
            dc = (2 / len(x)) * np.sum(error * x)
            dd = (2 / len(x)) * np.sum(error)

            self.play(
                a.animate.set_value(a.get_value() - lr * da),
                b.animate.set_value(b.get_value() - lr * db),
                c.animate.set_value(c.get_value() - lr * dc),
                d.animate.set_value(d.get_value() - lr * dd),
                run_time=0.08,
                rate_func=linear
            )

        self.wait(3)


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

