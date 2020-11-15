# -*- coding: utf-8 -*-
__author__ = 'Patricio Soriano @sigdeletras'
__date__ = '2020-11-15'

import processing
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterVectorLayer)


class ClipLayer(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            'CapaARecortar', 'Capa a recortar', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer(
            'CapaRecorte',
            'Capa Recorte',
            types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink(
            'CapaRecortada',
            'Capa recortada',
            type=QgsProcessing.TypeVectorAnyGeometry,
            createByDefault=True,
            defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Cortar
        alg_params = {
            'INPUT': parameters['CapaARecortar'],
            'OVERLAY': parameters['CapaRecorte'],
            'OUTPUT': parameters['CapaRecortada']
        }
        outputs['Cortar'] = processing.run(
            'native:clip', alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)
        results['CapaRecortada'] = outputs['Cortar']['OUTPUT']
        return results

    def name(self):
        return 'Recorte Capa'

    def displayName(self):
        return 'Recorte Capa'

    def group(self):
        return 'Vectoriales'

    def groupId(self):
        return 'vector'

    def createInstance(self):
        return ClipLayer()
