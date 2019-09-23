# pylint: disable=C0111, R0205
class Extractor(object):
    @classmethod
    def walk(cls, key, val_dict):
        if isinstance(key, str):
            return cls.walk(key.split('.'), val_dict)
        if len(key) > 1:
            val_dict_next = val_dict[key.pop(0)]
            return cls.walk(key, val_dict_next)
        return val_dict.get(key[0], '0')

    @classmethod
    def flatten(cls, dict_in):
        def expand(key, value):
            if isinstance(value, dict):
                return [(key + '.' + k, v)
                        for k, v in cls.flatten(value).items()]
            return [(key, value)]

        items = [item for k, v in dict_in.items() for item in expand(k, v)]

        return dict(items)

    @classmethod
    def flatten_to_list(cls, data):
        """
            New addition/ for ResourceFactory usage SPECIFICALLY.
            Flattens a dictionary of lists (only single lists, no nested lists accepted)
            :param data: Dictionary of list-like values
            :return: A flattened out list of values.
        """
        return [data.get(k)[i] for k in data.keys() for i in range(0, len(data.get(k)))]

