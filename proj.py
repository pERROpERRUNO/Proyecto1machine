from manim import *
import numpy as np


class RegressionDemo(Scene):
    def construct(self):
        # Secuencias de la animación
        self.introduccion()
        self.regresion_lineal_optimizada()
        self.regresion_no_lineal_optimizada()
        self.comparativa_final()
        self.conclusiones()

    def introduccion(self):
        titulo = Text("Análisis de Regresión", font_size=48, color=BLUE)
        subtitulo = Text("Modelado Lineal y No Lineal", font_size=32).next_to(titulo, DOWN)

        nombres = VGroup(
            Text("Grupo 6", font_size=24, color=GRAY),
            Text("Ricardo Meza • Miguel Ramos • Mateo Silva", font_size=20, color=GRAY)
        ).arrange(DOWN).to_edge(DOWN)

        self.play(Write(titulo))
        self.play(FadeIn(subtitulo, shift=UP))
        self.play(FadeIn(nombres))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(subtitulo), FadeOut(nombres))

    def regresion_lineal_optimizada(self):
        header = Title("1. Regresión Lineal Optimizada")
        self.add(header)

        ejes = Axes(x_range=[0, 10, 1], y_range=[0, 15, 2], axis_config={"include_tip": False}).scale(0.7).shift(
            DOWN * 0.5)

        # Datos
        x_pts = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        y_pts = np.array([2.1, 3.9, 5.2, 11.5, 7.1, 9.3, 10.2, 12.8, 14.1])
        puntos = VGroup(*[Dot(ejes.c2p(x, y), color=BLUE) for x, y in zip(x_pts, y_pts)])

        # Fórmulas LaTeX
        formula = MathTex("y = wx + b", color=YELLOW).to_corner(UL).shift(DOWN)
        loss_func = MathTex(r"MSE = \\frac{1}{n} \\sum (y_i - \hat{y}_i)^2", font_size=30).next_to(formula, DOWN,
                                                                                                  aligned_edge=LEFT)

        w = ValueTracker(0.1)
        b = ValueTracker(8.0)

        linea = always_redraw(lambda: ejes.plot(lambda x: w.get_value() * x + b.get_value(), color=YELLOW))

        # Visualización de error (Cuadrados)
        cuadrados = always_redraw(lambda: VGroup(*[
            Square(side_length=abs(ejes.c2p(0, y_pts[i])[1] - ejes.c2p(0, w.get_value() * x_pts[i] + b.get_value())[1]),
                   fill_opacity=0.2,
                   color=RED if abs(y_pts[i] - (w.get_value() * x_pts[i] + b.get_value())) > 2 else GREEN)
                                                 .move_to(
                ejes.c2p(x_pts[i], (y_pts[i] + w.get_value() * x_pts[i] + b.get_value()) / 2))
            for i in range(len(x_pts))
        ]))

        self.play(Create(ejes), Write(formula))
        self.play(FadeIn(puntos))
        self.play(Create(linea), FadeIn(cuadrados), Write(loss_func))
        self.wait(1)

        # Animación de optimización
        self.play(w.animate.set_value(1.35), b.animate.set_value(1.1), run_time=4)
        self.wait(2)
        self.play(FadeOut(VGroup(ejes, puntos, linea, cuadrados, formula, loss_func, header)))

    def regresion_no_lineal_optimizada(self):
        header = Title("2. Regresión No Lineal (Polinomial)")
        self.add(header)

        ejes = Axes(x_range=[0, 5, 1], y_range=[0, 20, 5]).scale(0.7).shift(DOWN * 0.5)

        # Datos curvos
        x_val = np.array([0.5, 1.2, 2.0, 2.8, 3.5, 4.2, 4.8])
        y_val = np.array([2.5, 3.1, 5.8, 10.2, 13.5, 17.2, 19.0])
        puntos = VGroup(*[Dot(ejes.c2p(x, y), color=PURPLE) for x, y in zip(x_val, y_val)])

        formula = MathTex("y = ax^2 + bx + c", color=PINK).to_corner(UL).shift(DOWN)

        # Simulamos la curvatura con un tracker
        curva_param = ValueTracker(0)  # Grado de curvatura

        curva = always_redraw(lambda: ejes.plot(
            lambda x: curva_param.get_value() * (x ** 2) + 0.5 * x + 2,
            color=PINK, x_range=[0, 5]
        ))

        self.play(Create(ejes), FadeIn(puntos), Write(formula))
        self.play(Create(curva))
        self.wait(3)

        # Optimización visual de la parábola
        self.play(curva_param.animate.set_value(0.7), run_time=4)
        self.wait(3)
        self.play(FadeOut(VGroup(ejes, puntos, curva, formula, header)))

    def comparativa_final(self):
        header = Title("3. Comparativa: Subajuste vs Ajuste")
        self.add(header)

        ejes = Axes(x_range=[0, 5, 1], y_range=[0, 20, 5]).scale(0.7)
        x_val = np.linspace(0.5, 4.5, 15)
        y_val = 1.2 * x_val ** 3 - 4 * x_val ** 2 + 5 * x_val + 2 + np.random.normal(0, 0.5, 15)
        puntos = VGroup(*[Dot(ejes.c2p(x, y), color=WHITE, radius=0.05) for x, y in zip(x_val, y_val)])

        linea = ejes.plot(lambda x: 2 * x + 3, color=RED)
        label_l = Text("Lineal (Underfitting)", color=RED, font_size=20).next_to(linea, UP)

        coefs = np.polyfit(x_val, y_val, 3)
        curva = ejes.plot(lambda x: coefs[0] * x ** 3 + coefs[1] * x ** 2 + coefs[2] * x + coefs[3], color=GREEN)
        label_nl = Text("No Lineal (Ideal)", color=GREEN, font_size=20).next_to(curva, RIGHT)

        self.play(Create(ejes), FadeIn(puntos))
        self.play(Create(linea), Write(label_l))
        self.wait(3)
        self.play(Create(curva), Write(label_nl), linea.animate.set_stroke(opacity=0.2))
        self.wait(3)
        self.play(FadeOut(VGroup(ejes, puntos, linea, curva, label_l, label_nl, header)))

    def conclusiones(self):
        titulo = Text("Conclusiones", color=BLUE).to_edge(UP)
        puntos = VGroup(
            Text("1. La Regresión Lineal es simple pero limitada.", font_size=28),
            Text("2. La Regresión No Lineal captura patrones complejos.", font_size=28),
            Text("3. El objetivo siempre es minimizar la función de pérdida.", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).shift(UP * 0.5)

        self.play(Write(titulo))
        for p in puntos:
            self.play(Write(p))
            self.wait(2)
        self.wait(4)
