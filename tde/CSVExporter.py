from tde.Exporter import Exporter
import csv


class CSVExporter(Exporter):
    """
    TODO: Refactoriser le contenu de cette classe + remonter dans Exporter
    """

    @staticmethod
    def _get_data_instance_header(data_instance):
        return [data_instance.get_key_name(), data_instance.get_value_name()]

    def export(self, output_directory, data_instances=True, implodes=True, errors=True):
        if data_instances:
            self.export_data_instances(output_directory)
        if implodes:
            self.export_implodes(output_directory)
        if errors:
            self.export_errors(output_directory)

    def export_data_instances(self, output_directory):
        for data_instance in self._data_collection.get_data_instances():

            data = data_instance.get_data()
            file_name = "%s.csv" % data_instance.get_name()
            file_path = "%s/%s" % (output_directory, file_name)

            # TODO: Create file and vider si existe
            with open(file_path, 'w') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
                writer.writerow(self._get_data_instance_header(data_instance))

                for data_key in data:
                    data_value = data[data_key]
                    writer.writerow([data_key, data_value])

    def export_implodes(self, output_directory):
        for implode_class in self._implode_classes:
            implode_data_instances = self._get_data_instance_where_class_are(implode_class.get_data_classes())
            implode = implode_class(implode_data_instances)

            file_name = "%s.csv" % implode.get_name()
            file_path = "%s/%s" % (output_directory, file_name)

            with open(file_path, 'w') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
                writer.writerow(implode.get_header())

                implode_data = implode.get_data()
                for data_key in implode_data:
                    data_values = implode_data[data_key]
                    data_row = [data_key]
                    data_row.extend(data_values)
                    writer.writerow(data_row)

    def _get_data_instance_where_class_are(self, data_classes):
        data_instances = []

        for data_instance in self._data_collection.get_data_instances():
            if type(data_instance) in data_classes:
                data_instances.append(data_instance)

        return data_instances

    def export_errors(self, output_directory):
        with open(output_directory + '/errors.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(('File path', 'Action', 'Error'))

            for error in self._data_collection.get_errors():
                writer.writerow(error.get_as_tuple())
