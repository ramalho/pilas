# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import sys
import pilas
from pilas import pilasversion

class Depurador(object):
    """Esta clase permite hacer depuraciones visuales.

    La depuracion visual en pilas consiste en poder mostrar informacion
    que generalmente es invisible a los jugadores. Por ejemplo, donde
    estan situados los puntos de control, los radios de colision etc.

    Esta clase administra varios modos depuracion, que son los
    que dibujan figuras geometricas.
    """

    def __init__(self, lienzo, fps):
        self.modos = []
        self.lienzo = lienzo
        ModoDepurador.grosor_de_lineas = 1
        self.fps = fps
        self.posicion_del_mouse = (0, 0)
        pilas.eventos.mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def cuando_mueve_el_mouse(self, evento):
        self.posicion_del_mouse = (evento.x, evento.y)
        return True

    def comienza_dibujado(self, motor, painter):
        for m in self.modos:
            m.comienza_dibujado(motor, painter, self.lienzo)

    def dibuja_al_actor(self, motor, painter, actor):
        for m in self.modos:
            m.dibuja_al_actor(motor, painter, self.lienzo, actor)

    def termina_dibujado(self, motor, painter):
        if self.modos:
            self._mostrar_cantidad_de_actores(painter)
            self._mostrar_cuadros_por_segundo(painter)
            self._mostrar_posicion_del_mouse(painter)
            self._mostrar_nombres_de_modos(painter)

            for m in self.modos:
                m.termina_dibujado(motor, painter, self.lienzo)

    def cuando_pulsa_tecla(self, evento):
        if evento.codigo == 'F6':
            pilas.eventos.imprimir_todos()
        elif evento.codigo == 'F7':
            self._alternar_modo(ModoInformacionDeSistema)
        elif evento.codigo == 'F8':
            self._alternar_modo(ModoPuntosDeControl)
        elif evento.codigo == 'F9':
            self._alternar_modo(ModoRadiosDeColision)
        elif evento.codigo == 'F10':
            self._alternar_modo(ModoArea)
        elif evento.codigo == 'F11':
            self._alternar_modo(ModoFisica)
        elif evento.codigo == 'F12':
            self._alternar_modo(ModoPosicion)
        elif evento.texto == '+':
            self._cambiar_grosor_de_bordes(+1)
        elif evento.texto == '-':
            self._cambiar_grosor_de_bordes(-1)

    def _cambiar_grosor_de_bordes(self, cambio):
        ModoDepurador.grosor_de_lineas = max(1, ModoDepurador.grosor_de_lineas + cambio)

    def _alternar_modo(self, clase_del_modo):
        clases_activas = [x.__class__ for x in self.modos]

        if clase_del_modo in clases_activas:
            self._desactivar_modo(clase_del_modo)
        else:
            self._activar_modo(clase_del_modo)

    def _activar_modo(self, clase_del_modo):
        pilas.eventos.inicia_modo_depuracion.emitir()
        instancia_del_modo = clase_del_modo(self)
        self.modos.append(instancia_del_modo)
        self.modos.sort(key=lambda x: x.orden_de_tecla())

    def _desactivar_modo(self, clase_del_modo):
        instancia_a_eliminar = [x for x in self.modos
                                if x.__class__ == clase_del_modo]
        self.modos.remove(instancia_a_eliminar[0])
        instancia_a_eliminar[0].sale_del_modo()

        if not self.modos:
            pilas.eventos.sale_modo_depuracion.emitir()

    def _mostrar_nombres_de_modos(self, painter):
        dy = 0
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()

        for modo in self.modos:
            texto = modo.tecla + " " + modo.__class__.__name__ + " habilitado."
            self.lienzo.texto_absoluto(painter, texto, izquierda + 10, arriba -20 +dy, color=pilas.colores.violeta)
            dy -= 20

    def _mostrar_posicion_del_mouse(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        x, y = self.posicion_del_mouse
        texto = u"Posición del mouse: x=%d y=%d " %(x, y)
        self.lienzo.texto_absoluto(painter, texto, derecha - 230, abajo + 10, color=pilas.colores.violeta)

    def _mostrar_cuadros_por_segundo(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        rendimiento = self.fps.obtener_cuadros_por_segundo()
        texto = "Cuadros por segundo: %s" %(rendimiento)
        self.lienzo.texto_absoluto(painter, texto, izquierda + 10, abajo + 10, color=pilas.colores.violeta)

    def _mostrar_cantidad_de_actores(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        total_de_actores = len(pilas.actores.todos)
        texto = "Cantidad de actores: %s" %(total_de_actores)
        self.lienzo.texto_absoluto(painter, texto, izquierda + 10, abajo + 30, color=pilas.colores.violeta)


class ModoDepurador(object):
    tecla = "F00"

    def __init__(self, depurador):
        self.depurador = depurador

    def comienza_dibujado(self, motor, painter, lienzo):
        pass

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        pass

    def termina_dibujado(self, motor, painter, lienzo):
        pass

    def orden_de_tecla(self):
        return int(self.tecla[1:])

    def sale_del_modo(self):
        pass


class ModoInformacionDeSistema(ModoDepurador):
    tecla = "F7"

    def __init__(self, depurador):
        ModoDepurador.__init__(self, depurador)

        self.informacion = [
            "Usando el motor: " + pilas.mundo.motor.nombre,
            "Sistema: " + sys.platform,
            "Version de pilas: " + pilasversion.VERSION,
            "Version de python: " + sys.subversion[0] + " " + sys.subversion[1],
            "Version de Box2D: " + pilas.fisica.obtener_version(),
            ]

    def termina_dibujado(self, motor, painter, lienzo):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()

        for (i, texto) in enumerate(self.informacion):
            posicion_y = abajo + 50 + i * 20
            lienzo.texto(painter, texto, izquierda + 10, posicion_y, color=pilas.colores.negro)


class ModoPuntosDeControl(ModoDepurador):
    tecla = "F8"

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        lienzo.cruz(painter, actor.x - pilas.mundo.camara.x, actor.y - pilas.mundo.camara.y, color=pilas.colores.rojo, grosor=ModoDepurador.grosor_de_lineas)


class ModoRadiosDeColision(ModoDepurador):
    tecla = "F9"

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        lienzo.circulo(painter, actor.x - pilas.mundo.camara.x, actor.y - pilas.mundo.camara.y, actor.radio_de_colision, color=pilas.colores.verde, grosor=ModoDepurador.grosor_de_lineas)


class ModoArea(ModoDepurador):
    tecla = "F10"

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        dx, dy = actor.centro
        lienzo.rectangulo(painter, actor.x - dx - pilas.mundo.camara.x, actor.y + dy - pilas.mundo.camara.y, actor.ancho, actor.alto, color=pilas.colores.azul, grosor=ModoDepurador.grosor_de_lineas)


class ModoFisica(ModoDepurador):
    tecla = "F11"

    def termina_dibujado(self, motor, painter, lienzo):
        grosor = ModoDepurador.grosor_de_lineas
        pilas.mundo.fisica.dibujar_figuras_sobre_lienzo(painter, lienzo, grosor)


class ModoPosicion(ModoDepurador):
    tecla = "F12"

    def __init__(self, depurador):
        ModoDepurador.__init__(self, depurador)
        self.eje = pilas.actores.Ejes()

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        if not isinstance(actor, pilas.fondos.Fondo):
            texto = "(%d, %d)" %(actor.x, actor.y)
            lienzo.texto(painter, texto, actor.derecha - pilas.mundo.camara.x, actor.abajo - pilas.mundo.camara.y, color=pilas.colores.violeta)

    def sale_del_modo(self):
        self.eje.eliminar()
