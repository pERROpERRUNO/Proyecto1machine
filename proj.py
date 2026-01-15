from manim import *
import numpy as np

class RegressionDemo(Scene):
    def construct(self):
        self.show_title()
        self.linear_regression()
        self.nonlinear_regression()
        self.wait(2)

    def show_title(self):
        title = Text(
            "Linear and Nonlinear Regression",
            font_size=42
        ).to_edge(UP)

        subtitle = Text(
            "Grupo 6 – Integrantes:",
            font_size=28
        )

        members = VGroup(
            Text("Meza León, Ricardo Manuel", font_size=24),
            Text("Ramos Bonilla, Miguel Angel", font_size=24),
            Text("Silva Azañero, Mateo Alejandro", font_size=24)
        ).arrange(DOWN, buff=0.2)

        info = VGroup(subtitle, members).arrange(DOWN, buff=0.4)
        info.next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(title, shift=DOWN))
        self.play(LaggedStart(*[FadeIn(obj) for obj in info], lag_ratio=0.2))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(info))

    def linear_regression(self):
        header = Text("Linear Regression", font_size=36).to_edge(UP)
        self.play(Write(header))

        
        x = np.linspace(0, 10, 30)
        y = 1.2 * x + 2 + np.random.normal(0, 0.5 + 0.1*x, len(x))  # ruido creciente
        y[5] += 3  # outlier puntual
        coef = np.polyfit(x, y, 1)

       
        model_text = Text("Model:  y = w·x + b", font_size=28)
        loss_text = Text("Loss:  L = (1/N) Σ (y − ŷ)²", font_size=28)
        values_text = Text(
            f"Learned model:  y = {coef[0]:.2f}·x + {coef[1]:.2f}",
            font_size=26
        )

        formulas = VGroup(model_text, loss_text, values_text).arrange(DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(f) for f in formulas], lag_ratio=0.3))
        self.wait(2)
        self.play(FadeOut(formulas))

        
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 15, 1],
            axis_config={"color": WHITE},
            tips=False
        ).shift(DOWN * 0.5)

        axes.get_x_axis().add_numbers(font_size=20)
        axes.get_y_axis().add_numbers(font_size=20)
        labels = axes.get_axis_labels(Text("x"), Text("y"))

        self.play(Create(axes), Write(labels))

       
        points = VGroup(*[Dot(axes.c2p(x[i], y[i]), radius=0.05, color=BLUE) for i in range(len(x))])
        self.play(LaggedStartMap(FadeIn, points, lag_ratio=0.05, run_time=1.5))

        
        reg_line = axes.plot(lambda t: coef[0]*t + coef[1], x_range=[0, 10], color=RED)
        self.play(Create(reg_line))
        self.wait(2)

      
        residuals = VGroup(*[
            Line(
                axes.c2p(x[i], y[i]),
                axes.c2p(x[i], coef[0]*x[i] + coef[1]),
                color=YELLOW,
                stroke_width=2
            ) for i in range(len(x))
        ])
        self.play(LaggedStartMap(Create, residuals, lag_ratio=0.05))
        self.wait(2)

        self.play(
            FadeOut(points),
            FadeOut(reg_line),
            FadeOut(residuals),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(header)
        )

    def nonlinear_regression(self):
        header = Text("Nonlinear Regression (Polynomial)", font_size=36).to_edge(UP)
        self.play(Write(header))

       
        x = np.linspace(0, 4, 40)
        y = 0.5*x**3 - 2*x**2 + 3*x + 1 + np.random.normal(0, 0.5 + 0.2*x, len(x))
        coef = np.polyfit(x, y, 3)

        
        model_text = Text("Model:  y = a·x³ + b·x² + c·x + d", font_size=28)
        loss_text = Text("Loss:  L = (1/N) Σ (y − ŷ)²", font_size=28)
        values_text = Text(
            f"Learned model:  y = {coef[0]:.2f}·x³ + {coef[1]:.2f}·x² + {coef[2]:.2f}·x + {coef[3]:.2f}",
            font_size=26
        )

        formulas = VGroup(model_text, loss_text, values_text).arrange(DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(f) for f in formulas], lag_ratio=0.3))
        self.wait(2)
        self.play(FadeOut(formulas))

        
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 10, 2],  # límite máximo en 10
            axis_config={"color": WHITE},
            tips=False
        ).shift(DOWN * 0.5)

        axes.get_x_axis().add_numbers(font_size=20)
        axes.get_y_axis().add_numbers(font_size=20)
        labels = axes.get_axis_labels(Text("x"), Text("y"))

        self.play(Create(axes), Write(labels))

       
        points = VGroup(*[Dot(axes.c2p(x[i], y[i]), radius=0.05, color=GREEN) for i in range(len(x))])
        self.play(LaggedStartMap(FadeIn, points, lag_ratio=0.05, run_time=1.5))

        
        poly_curve = axes.plot(
            lambda t: min(coef[0]*t**3 + coef[1]*t**2 + coef[2]*t + coef[3], 10),
            x_range=[0, 4],
            color=YELLOW
        )
        self.play(Create(poly_curve))
        self.wait(2)

        
        # Mostrar residuos
        
        residuals = VGroup(*[
            Line(
                axes.c2p(x[i], y[i]),
                axes.c2p(x[i], min(coef[0]*x[i]**3 + coef[1]*x[i]**2 + coef[2]*x[i] + coef[3], 10)),
                color=RED,
                stroke_width=2
            ) for i in range(len(x))
        ])
        self.play(LaggedStartMap(Create, residuals, lag_ratio=0.05))
        self.wait(3)

        self.play(
            FadeOut(points),
            FadeOut(poly_curve),
            FadeOut(residuals),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(header)
        )
